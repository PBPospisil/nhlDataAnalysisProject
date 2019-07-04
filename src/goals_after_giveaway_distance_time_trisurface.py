from graph_goals_after_giveaway_3d_time_distance import GraphTimeDistanceGiveawayGoalsTrisurface


xlabel='time'; ylabel='distance'; plot_file_name='../img/less-than-60sec.mp4'
title = 'Time and distance distribution for goals scored < 60 sec after giveaway'
animated_giveaway_goal_trisurface = GraphTimeDistanceGiveawayGoalsTrisurface()
animated_giveaway_goal_trisurface.get_time_and_distance(max_time=60)
animated_giveaway_goal_trisurface.create_and_save_plot(xlabel, ylabel, title, plot_file_name)
