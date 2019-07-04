from graph_team_gaa import GraphTeamGaa
from ui import UiElement


def main():
    team_gaa = GraphTeamGaa()
    team_gaa.sort_goalie_stats_by_game_id()
    team_gaa.get_team_from_user(UiElement().show_team_menu(team_gaa))
    team_gaa.add_gaa_toi_columns()
    team_gaa.create_plot_and_save()

if __name__ == '__main__':
    main()
