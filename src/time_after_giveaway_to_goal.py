from graph_goals_after_giveaway_density import GraphGiveawayGoals


def main():
    xlabel = 'time (min)'; ylabel = 'density'
    title = 'density plot and histogram of time to score after giveaway'
    plot_file_name = '../img/density-plot-time-to-score-after-giveaway.png'

    giveaway_goals_time_density_plot = GraphGiveawayGoals(subset='goals_after_giveaway')
    giveaway_goals_time_density_plot.get_giveaway_stats()
    giveaway_goals_time_density_plot.save_giveaway_goal_csv()
    giveaway_goals_time_density_plot.create_and_save_plot(xlabel, ylabel, title, plot_file_name, mode='time')

if __name__ == '__main__':
    main()
