from graph_model import GraphModel
from ui import UiElement


# initialize classes
win_prediction = GraphModel()
user_options = UiElement()

# filter for just regular season games
win_prediction.only_regular_season(win_prediction.goalie_stats)
win_prediction.only_regular_season(win_prediction.team_stats)

# get season for each game for goalies
win_prediction.get_seasons(win_prediction.goalie_stats)

# get season for each game for teams
win_prediction.get_seasons(win_prediction.team_stats)

# create unique ID for team-season
win_prediction.create_unique_team_season_identifier(win_prediction.goalie_stats)

# initialize dataframe such that each row is team-season unique
win_prediction.create_team_season()

# fill team-season dataframe
win_prediction.fill_team_season()

# UI handling
user_options.menu_and_save_graph(win_prediction)
