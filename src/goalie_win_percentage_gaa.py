from graph_goalie_stats import GraphGoalieStats


# initialize classes
mode='GAA'
if mode == 'GAA':
    figure_name = '../img/goalie-gaa-winpercentage-regplot.png'
else:
    figure_name = '../img/goalie-svpercentage-winpercentage-regplot.png'
goalie_gaa_win_percentage = GraphGoalieStats(mode=mode, figure_name=figure_name)

# filter for just regular season games
goalie_gaa_win_percentage.only_regular_season(goalie_gaa_win_percentage.goalie_stats)
goalie_gaa_win_percentage.only_regular_season(goalie_gaa_win_percentage.team_stats)

# get season for each game for goalies
goalie_gaa_win_percentage.get_seasons(goalie_gaa_win_percentage.goalie_stats)

# get season for each game for teams
goalie_gaa_win_percentage.get_seasons(goalie_gaa_win_percentage.team_stats)

# create unique ID for team-season
goalie_gaa_win_percentage.create_unique_goalie_season_identifier(goalie_gaa_win_percentage.goalie_stats)

# initialize dataframe such that each row is team-season unique
goalie_gaa_win_percentage.create_goalie_season()

# fill team-season dataframe
goalie_gaa_win_percentage.fill_goalie_season()


goalie_gaa_win_percentage.graph_regplot()
