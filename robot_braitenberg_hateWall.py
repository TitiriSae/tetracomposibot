from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "Braitenberg Avoider"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        sensor_to_wall = []
        sensor_to_enemy = []
        sensor_to_ally = []

        for i in range (0,8):
            # Si le capteur perçoit un mur, ajoute la distance au mur
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_enemy.append(1.0)
                sensor_to_ally.append(1.0)

            # Si le capteur perçoit un robot, ajoute la distance au robot selon si c'est un ennemi ou un allié
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                if sensor_team[i] == self.team_name:
                    sensor_to_ally.append(sensors[i])
                    sensor_to_enemy.append(1.0)
                else:
                    sensor_to_ally.append(1.0)
                    sensor_to_enemy.append(sensors[i])
            # Si le capteur ne perçoit rien
            else:
                sensor_to_wall.append(1.0)
                sensor_to_enemy.append(1.0)
                sensor_to_ally.append(1.0)

        DISTANCE_WALL = 0.2
        DISTANEC_ROBOT = 0.2
        
        stuck_front = sensors[sensor_front] < DISTANCE_WALL 
        stuck_left = sensors[sensor_left] < DISTANCE_WALL
        stuck_right = sensors[sensor_right] < DISTANCE_WALL

        is_followed = sensor_to_enemy[sensor_rear] != 1.0 or sensor_to_enemy[sensor_rear_left] != 1.0 or sensor_to_enemy[sensor_rear_right] != 1.0
        


        # if debug == True:
        #     if self.iteration % 100 == 0:
        #         print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
        #         print ("\tsensors (distance, max is 1.0)  =",sensors)
        #         print ("\t\tsensors to wall  =",sensor_to_wall)
        #         print ("\t\tsensors to robot =",sensor_to_robot)
        #         print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
        #         print ("\trobot's name (if relevant)      =",sensor_robot)
        #         print ("\trobot's team (if relevant)      =",sensor_team)

        translation = sensors[sensor_front]*0.5 # A MODIFIERœ
        rotation = (-1)*(1-sensor_to_wall[sensor_front_left]) + (1)*(1-sensor_to_wall[sensor_front_right]) + choice([-1, 1])*(1-sensor_to_wall[sensor_front]) # A MODIFIER

        self.iteration = self.iteration + 1        
        return translation, rotation, False
