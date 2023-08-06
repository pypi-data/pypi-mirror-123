from .leagueinfo import LeagueInfo
from .managerinfo import ManagerInfo
from .playerinfo import PlayerInfo

import logging

logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('matplotlib.pyplot').setLevel(logging.WARNING)
