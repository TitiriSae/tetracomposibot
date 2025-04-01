# Configuration file.

import arenas

# general -- first three parameters can be overwritten with command-line arguments (cf. "python tetracomposibot.py --help")

display_mode = 0
arena = 0
position = False 
max_iterations = 501*10 #401*500

# affichage

display_welcome_message = True
verbose_minimal_progress = True # display iterations
display_robot_stats = True
display_team_stats = True
display_tournament_results = True
display_time_stats = True

# initialization : create and place robots at initial positions (returns a list containing the robots)

import robot_braitenberg_hateBot as robot_strat1
import robot_braitenberg_loveBot as robot_strat2

def initialize_robots(arena_size=-1, particle_box=-1): # particle_box: size of the robot enclosed in a square
    x_center = arena_size // 2 - particle_box / 2
    y_center = arena_size // 2 - particle_box / 2
    robots = []
    robots.append(robot_strat1.Robot_player(4, y_center, 0, name="First Robot", team="Team Wander"))
    robots.append(robot_strat1.Robot_player(93, y_center, 180, name="Second robot", team="Team Wander"))
    robots.append(robot_strat2.Robot_player(x_center, y_center+20, 90, name="Third robot", team="Team Dumb"))
    robots.append(robot_strat2.Robot_player(x_center, y_center-40, 270, name="Fourth robot", team="Team Dumb"))
    return robots
