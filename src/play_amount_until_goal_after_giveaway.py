from graph_goals_after_giveaway_density import GraphGiveawayGoals


def main():
    xlabel = 'plays after giveaway'; ylabel = 'density'
    title = 'density plot and histogram of plays until goal scored after giveaway'
    plot_file_name = '../img/density-plot-plays-unitl-goal-after-giveaway.png

    giveaway_goals_count_density_plot = GraphGiveawayGoals(subset='goals_after_giveaway')
    giveaway_goals_count_density_plot.get_giveaway_stats()
    giveaway_goals_count_density_plot.save_giveaway_goal_csv()
    giveaway_goals_count_density_plot.create_and_save_plot(xlabel, ylabel, title, plot_file_name, mode='count')

if __name__ == '__main__':
    main()
