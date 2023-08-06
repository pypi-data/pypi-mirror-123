import objectpath
import yahoo_fantasy_api as yfa
from deez_stats.pyquery import database_query as dbq
from deez_stats.pyquery import yahoo_query as yq
from deez_stats.pyquery import json_query as jq
from deez_stats.weekly_matchup import WeeklyMatchup


class LeagueInfo:
    """A snapshot in time (SIT) for all the league info at a given season and week

    :param sc: Fully constructed session context
    :type sc: :class:`yahoo_oauth.OAuth2`
    :param season: the season of interest
    :type season: int, optional
    :param week: the week of interest
    :type week: int, optional
    """
    def __init__(self, sc, season=None, week=None):
        self.sc = sc
        self.league_key = None
        self.league_id = None
        self.name = None
        self.persistent_url = None
        self.logo_url = None
        self.num_teams = None
        self.num_matchups = None
        self.week = week
        self.current_week = None
        self.start_week = None
        self.start_date = None
        self.end_week = None
        self.end_date = None
        self.game_id = None
        self.season = season
        self.current_season = None
        self.weekly_matchups = None
        self.weekly_matchup_histories = None
        self.manager_names = None
        self.playoff_start_week = None
        self.trade_end_date = None
        self.sendbird_channel_url = None
        self.league = None
        self.roster_positions = None
        self.stat_categories = None
        self._update_LeagueInfo()

    def get_weekly_matchups(self):
        """Creates a list of weekly matchup objects for the main class

        """
        matchups_raw = yfa.League(self.sc, self.league_key).matchups(week=self.week)
        tree = objectpath.Tree(matchups_raw)
        team_ids = list(map(int, list(tree.execute('$..team_id'))))
        team_points_total = list(map(float, list(tree.execute('$..team_points.total'))))
        win_probability = list(map(float, list(tree.execute('$..win_probability'))))
        team_projected_points = list(map(float, list(tree.execute('$..team_projected_points.total'))))

        self.weekly_matchups = []
        for i in range(self.num_matchups):
            wm = WeeklyMatchup()

            m_index = 2 * i
            wm.manager_id = team_ids[m_index]
            wm.manager_name = self.manager_names[wm.manager_id]
            wm.manager_points_total = team_points_total[m_index]
            wm.manager_win_probability = int(win_probability[m_index] * 100)
            wm.manager_projected_points = team_projected_points[m_index]
            # wm.manager_elo = dbq.get_manager_elo(self.season, self.week, wm.manager_name)

            o_index = 2 * i + 1
            wm.opponent_id = team_ids[o_index]
            wm.opponent_name = self.manager_names[wm.opponent_id]
            wm.opponent_points_total = team_points_total[o_index]
            wm.opponent_win_probability = int(win_probability[o_index] * 100)
            wm.opponent_projected_points = team_projected_points[o_index]
            # wm.opponent_elo = dbq.get_manager_elo(self.season, self.week, wm.opponent_name)

            self.weekly_matchups.append(wm)

    def get_weekly_matchup_histories(self):
        """Creates a list of historical matchup info objects for the main class

        """
        self.weekly_matchup_histories = []
        for matchup in self.weekly_matchups:
            mh = dbq.get_matchup_history(matchup.manager_name, matchup.opponent_name)
            self.weekly_matchup_histories.append(mh)

    def get_manager_names(self):
        """Finders current manager names from Yahoo and cleanly formats them

        """
        nicknames = self.league.yhandler.get_standings_raw(self.league_key)
        tree = objectpath.Tree(nicknames)
        ids = list(map(int, list(tree.execute('$..manager_id'))))
        nicknames = list(tree.execute('$..nickname'))
        self.manager_names = dict(zip(ids, nicknames))
        self._clean_manager_names()

    def display_matchup_info(self):
        """ASCII visual of class data and formatting examples

        """
        for wm, mh in zip(self.weekly_matchups, self.weekly_matchup_histories):
            print("{:>10} | {:6.2f}\t {:6.2f} | {:<10}\
                ".format(wm.manager_name, wm.manager_points_total,
                wm.opponent_points_total, wm.opponent_name))
            print(" projected | {:6.2f}\t {:6.2f} | projected\
                ".format(wm.manager_projected_points, wm.opponent_projected_points))
            print("  win prob | {:5d}%\t {:5d}% | win prob\
                ".format(wm.manager_win_probability, wm.opponent_win_probability))
            # print("   ranking | {:6d}\t {:6d} | ranking\
            #     ".format(wm.manager_elo, wm.opponent_elo))
            print("The current record between {} and {} is {} - {}. \
                ".format(mh.manager_name, mh.opponent_name, mh.manager_wins, mh.opponent_wins))
            print("The average score between {} and {} is {:0.2f} - {:0.2f}.\
                ".format(mh.manager_name, mh.opponent_name, mh.manager_avg_score, mh.opponent_avg_score))
            print(mh.matchup_history_df)
            print("*********************************************************************")

    def _clean_manager_names(self):
        """Handles formatting names since there is no uniformity

        """
        cleaned_names = jq.get_cleaned_names()
        for key, value in self.manager_names.items():
            try:
                self.manager_names[key] = cleaned_names[value]
            except KeyError:  # not everyone's name is wrong so pass on the correct names
                pass

    def _get_current_season(self):
        """Finds the current season from Yahoo if season isn't provided

        :return: current season
        :rtype: int
        """
        raw_game_data = yq.yahoo_query(self.sc, 'game/nfl')
        return int(list(jq.search_json_key(raw_game_data, '..season'))[0])

    def _get_league_key_from_season(self):
        """Looks up league key specific for a specific season

        :return: formatted league key
        :rtype: list(int)
        """
        ids = jq.get_game_league_ids(self.season)
        return '{}.l.{}'.format(ids[0], ids[1])

    def _get_roster_positions(self):
        """Gets dict of eligible positions

        :return: dict of positions
        :rtype: dict
        """
        raw_settings = self.league.yhandler.get_settings_raw(self.league_key)
        tree = objectpath.Tree(raw_settings)
        positions = list(tree.execute('$..roster_position.position'))
        counts = map(int, list(tree.execute('$..roster_position.count')))
        return dict(zip(positions, counts))

    def _get_stats(self):
        """Gets stat categories and modifiers

        :return: dict of stat info
        :rtype: dict
        """
        data = self.league.yhandler.get_settings_raw(self.league_key)
        tree = objectpath.Tree(data)
        stat_categories = list(tree.execute('$..settings.stat_categories'))[0]
        stat_modifiers = list(tree.execute('$..settings.stat_modifiers'))[0]
        # it's in two different locations in two different orders, just create two trees
        sc_tree = objectpath.Tree(stat_categories)
        sm_tree = objectpath.Tree(stat_modifiers)

        stats = {}
        for i in range(100):
            name = list(sc_tree.execute('$.stats.stat[@.stat_id is {}].name'.format(i)))
            if name:
                stat_id = i
                name = name[0]
                display_name = list(sc_tree.execute('$.stats.stat[@.stat_id is {}].display_name'.format(i)))[0]

                try:
                    value = float(list(sm_tree.execute('$.stats.stat[@.stat_id is {}].value'.format(i)))[0])
                except IndexError:
                    value = 0
                try:
                    target = float(list(sm_tree.execute('$.stats.stat[@.stat_id is {}].bonuses..bonus.target'.format(i)))[0])
                except IndexError:
                    target = 0
                try:
                    points = float(list(sm_tree.execute('$.stats.stat[@.stat_id is {}].bonuses..bonus.points'.format(i)))[0])
                except IndexError:
                    points = 0
                stats[stat_id] = {'name': name, 'display_name': display_name, 'value': value, 'bonus_target': target, 'bonus_points': points}
        return stats

    def _update_LeagueInfo(self):
        """Main method to update the LeagueInfo class with SIT data

        """
        self.current_season = self._get_current_season()

        if self.season is None:  # grab current season
            self.season = self.current_season

        self.league_key = self._get_league_key_from_season()
        self.league = yfa.League(self.sc, self.league_key)
        settings = self.league.settings()
        self.league_id = jq.search_json_key(settings, '.league_id')
        self.name = jq.search_json_key(settings, '.name')
        self.logo_url = jq.search_json_key(settings, '.logo_url')
        self.num_teams = jq.search_json_key(settings, '.num_teams')
        self.num_matchups = self.num_teams // 2
        self.current_week = jq.search_json_key(settings, '.current_week')
        self.start_week = int(jq.search_json_key(settings, '.start_week'))
        self.start_date = jq.search_json_key(settings, '.start_date')
        self.end_week = int(jq.search_json_key(settings, '.end_week'))
        self.end_date = jq.search_json_key(settings, '.end_date')
        self.game_code = jq.search_json_key(settings, '.game_code')
        self.persistent_url = jq.search_json_key(settings, '.persistent_url')
        self.playoff_start_week = jq.search_json_key(settings, '.playoff_start_week')
        self.trade_end_date = jq.search_json_key(settings, '.trade_end_date')
        self.sendbird_channel_url = jq.search_json_key(settings, '.sendbird_channel_url')
        self.roster_positions = self._get_roster_positions()
        self.stats = self._get_stats()

        if self.week is None:  # grab current week
            self.week = self.current_week

        self.get_manager_names()
        self.get_weekly_matchups()
        self.get_weekly_matchup_histories()
