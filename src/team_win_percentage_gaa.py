from graph_team_stats import GraphTeamStats


team_gaa_win_percentage = GraphTeamStats()

team_gaa_win_percentage.only_regular_season(team_gaa_win_percentage.goalie_stats)
team_gaa_win_percentage.only_regular_season(team_gaa_win_percentage.team_stats)

team_gaa_win_percentage.get_seasons(team_gaa_win_percentage.goalie_stats)

# get season for each game for teams
team_gaa_win_percentage.get_seasons(team_gaa_win_percentage.team_stats)

# create unique ID for team-season
team_gaa_win_percentage.create_unique_team_season_identifier(team_gaa_win_percentage.goalie_stats)

# initialize dataframe such that each row is team-season unique
team_gaa_win_percentage.create_team_season()

# fill team-season dataframe
team_gaa_win_percentage.fill_team_season()

team_gaa_win_percentage.games_played_minimum(60)

team_gaa_win_percentage.create_plot_and_save()
