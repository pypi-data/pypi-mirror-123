import sqlite3
import pandas as pd
import pathlib
from deez_stats.telo.telo import Elo
from deez_stats.matchup_history import MatchupHistory

INIT_ELO = 700
HERE = (pathlib.Path(__file__).parent)
DATABASE_FILE = (HERE / 'files/database/history.db')


def execute_sqlite(sql_query):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    result = cursor.execute(sql_query)
    result = list(result)
    cursor.close()
    connection.close()
    return result


def execute_commit(sql_query):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    result = cursor.execute(sql_query)
    result = list(result)
    cursor.close()
    connection.commit()
    connection.close()
    return result


def execute_row_factory(sql_query):
    connection = sqlite3.connect(DATABASE_FILE)
    # connection.row_factory = lambda cursor, row: row[0]
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    result = cursor.execute(sql_query)
    # result = list(result)
    cursor.close()
    connection.close()
    print(result)
    return result


def get_matchup_history(manager_name, opponent_name):
    """Gets all of the historical matchups and run some basic stats

    """
    mh = MatchupHistory(manager_name, opponent_name)

    all_historical_matchups = find_all_historical_matchups(manager_name, opponent_name)

    columns = ['Season', 'Manager Score', 'Opponent Score', 'Result']
    mh.matchup_history_df = pd.DataFrame(all_historical_matchups, columns=columns)

    mh.manager_avg_score = mh.matchup_history_df['Manager Score'].mean()
    mh.opponent_avg_score = mh.matchup_history_df['Opponent Score'].mean()

    try:
        mh.manager_wins = mh.matchup_history_df.Result.value_counts().W
    except AttributeError:
        mh.manager_wins = 0

    try:
        mh.opponent_wins = mh.matchup_history_df.Result.value_counts().L
    except AttributeError:
        mh.opponent_wins = 0
    return mh


def find_all_historical_matchups(manager_name, opponent_name):
    """Finds all of the historical matchups in the database

    """
    query_string = '''
        SELECT  season,
                manager_score,
                opponent_score,
                result
        FROM    schedule
        WHERE   manager_name = "{}" AND opponent_name = "{}"
    '''.format(manager_name, opponent_name)
    result = execute_sqlite(query_string)
    return result


def update_weekly_results(li, update=False):
    # if leagueinfo.end_week - week == 1:  # check if semifinals
    #     d = find_weekly_winners(season=season, week=week - 1)
    #     quarterfinal_winners = [i[0] for i in d]
    #     semifinals = []
    #     matchups = leagueinfo.weekly_matchups
    #     for idx, name in enumerate(matchups):
    #         if name[0] not in quarterfinal_winners:
    #             if idx % 2 == 0:
    #                 if matchups[idx + 1][0] in quarterfinal_winners:
    #                     semifinals.append(name)
    #             else:
    #                 if matchups[idx - 1][0] in quarterfinal_winners:
    #                     semifinals.append(name)
    #         if name[0] in quarterfinal_winners:
    #             semifinals.append(name)
    #     leagueinfo.weekly_matchups = semifinals
    # elif leagueinfo.end_week - week == 0:  # check if finals
    #     d = find_seminfinal_managers(season=season, week=week - 1)
    #     semifinal_names = [i[0] for i in d]
    #     finals = []
    #     matchups = leagueinfo.weekly_matchups
    #     for idx, name in enumerate(matchups):
    #         if name[0] in semifinal_names:
    #             finals.append(name)
    #     leagueinfo.weekly_matchups = finals

    for i in range(len(li.weekly_matchups)):
        row = [li.season]
        row.append(li.week)
        row.append(li.weekly_matchups[i].manager_name)
        row.append(li.weekly_matchups[i].manager_points_total)
        row.append(li.weekly_matchups[i].opponent_name)
        row.append(li.weekly_matchups[i].opponent_points_total)
        if li.weekly_matchups[i].manager_points_total > li.weekly_matchups[i].opponent_points_total:
            row.append('W')
        else:
            row.append('L')
        # m_elo = get_manager_elo(li.season, li.week, li.weekly_matchups[i].manager_name)
        # o_elo = get_manager_elo(li.season, li.week, li.weekly_matchups[i].opponent_name)
        # row.append(m_elo)
        if update is True:
            update_database_row(row)

        row = [li.season]
        row.append(li.week)
        row.append(li.weekly_matchups[i].opponent_name)
        row.append(li.weekly_matchups[i].opponent_points_total)
        row.append(li.weekly_matchups[i].manager_name)
        row.append(li.weekly_matchups[i].manager_points_total)
        if li.weekly_matchups[i].opponent_points_total > li.weekly_matchups[i].manager_points_total:
            row.append('W')
        else:
            row.append('L')
        # o_elo = get_manager_elo(li.season, li.week, li.weekly_matchups[i].opponent_name)
        # row.append(m_elo)
        if update is True:
            update_database_row(row)


def update_database_row(row):
    query_string = '''
        INSERT INTO     schedule (
                        season,
                        week,
                        manager_name,
                        manager_score,
                        opponent_name,
                        opponent_score,
                        result,
                        elo)
        VALUES          ({}, {}, '{}', {}, '{}', {}, '{}', NULL)
    '''.format(*row)
    execute_commit(query_string)


def get_past_matchups(season, week):
    query_string = '''
        SELECT  *
        FROM    schedule
        WHERE   season = "{}" AND week = "{}"
    '''.format(season, week)
    result = execute_sqlite(query_string)
    return result


def find_weekly_winners(season, week):
    query_string = '''
        SELECT  manager_name, manager_score
        FROM    schedule
        WHERE   season = {} AND week = {} AND result = "W"
    '''.format(season, week)
    result = execute_sqlite(query_string)
    return result


def find_seminfinal_managers(season, week):
    query_string = '''
        SELECT  manager_name, manager_score
        FROM    schedule
        WHERE   season = {} AND week = {}
    '''.format(season, week)
    result = execute_sqlite(query_string)
    return result


def get_table_column_names(table):
    query_string = '''
        PRAGMA table_info({})
    '''.format(table)
    result = execute_sqlite(query_string)
    result = [i[1] for i in result]
    return result


def update_database_elo(season, week, manager_name, elo):
    query_string = '''
        UPDATE  schedule
        SET     elo={}
        WHERE   season={} AND week={} and manager_name="{}"
    '''.format(elo, season, week, manager_name)
    execute_commit(query_string)


def get_manager_elo(season, week, manager_name):
    if week - 1 == 0:
        if season > 2020:
            week = 18
        else:
            week = 17
        season = season - 1
    query_string = '''
        SELECT  elo
        FROM    schedule
        WHERE   season = {} AND week = {} AND manager_name="{}"
    '''.format(season, week - 1, manager_name)
    result = execute_sqlite(query_string)
    if result:
        result = result[0][0]
    return result


def update_weekly_elo(season, week, update=False, display=True):
    manager_elo = 0
    opponent_elo = 0
    prev_year = False

    current_week_df = get_weekly_df(season, week)

    for idx in range(len(current_week_df)):
        if season == 2015 and week == 1:
            manager_elo = INIT_ELO  # only for year 1 week 1
            opponent_elo = INIT_ELO
        else:
            if (week - 1) == 0:
                season = season - 1
                week = 17
                prev_year = True

            manager_name = current_week_df.at[idx, 'manager_name']
            opponent_name = current_week_df.at[idx, 'opponent_name']

            manager_elo = get_manager_elo(season, week - 1, manager_name)
            opponent_elo = get_manager_elo(season, week - 1, opponent_name)

            week_offset = 2
            while not (manager_elo):  # keep looking back in previous weeks
                try:
                    manager_elo = get_manager_elo(season, week - week_offset, manager_name)
                except IndexError:
                    pass
                finally:
                    week_offset = week_offset + 1
                if week_offset > 100:
                    manager_elo = INIT_ELO

            week_offset = 2
            while not (opponent_elo):  # keep looking back in previous weeks
                try:
                    opponent_elo = get_manager_elo(season, week - week_offset, opponent_name)
                except IndexError:
                    pass
                finally:
                    week_offset = week_offset + 1
                if week_offset > 100:
                    opponent_elo = INIT_ELO

        if prev_year:
            season = season + 1
            week = 1
            prev_year = False

        elo = Elo(manager_elo)
        elo.player_outcome(opponent_elo, current_week_df.at[idx, 'result'])
        current_week_df.at[idx, 'elo'] = elo.RpA
        if update is True:
            update_database_elo(season, week, current_week_df.at[idx, 'manager_name'], elo.RpA)
        if display is True:
            print('{}: {}\t{}: {}\t{}'.format(manager_name, elo.RpA, opponent_name, elo.RpB, elo.RpA - manager_elo))


def get_weekly_df(season, week):
    current_week_df = pd.DataFrame(get_past_matchups(season, week))
    current_week_df.columns = get_table_column_names('schedule')
    return current_week_df


def _get_previous_week_season(current_week, current_season, prev_year=False):
    if (current_week - 1) == 0:
        season = current_season - 1
        if season > 2020:
            week = 18
        else:
            week = 17
        prev_year = True
    else:
        week = current_week - 1
        season = current_season
        prev_year = False

    return [week, season, prev_year]

# def find_previous_week(current_week, current_season):

# miscellaneous functions that may be helpful

# def get_manager_score_history(manager_name):
#     query_string = '''
#         SELECT  manager_score
#         FROM    schedule
#         WHERE   manager_name = "{}"
#         ORDER BY manager_score DESC;
#     '''.format(manager_name)
#     result = execute_row_factory(query_string)
#     return result
