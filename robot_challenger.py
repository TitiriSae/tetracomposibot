# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Eric ZHENG 21205768
#  Prénom Nom No_étudiant/e : Thierry SAE LIM
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 
import math

nb_robots = 0

class Robot_player(Robot):

    team_name = "Inkling"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

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

        DISTANCE_WALL = 0.1
        
        stuck_front = sensors[sensor_front] < DISTANCE_WALL  
        stuck_left = sensors[sensor_left] < DISTANCE_WALL
        stuck_right = sensors[sensor_right] < DISTANCE_WALL
        stuck_front_left = sensors[sensor_front_left] < DISTANCE_WALL
        stuck_front_right = sensors[sensor_front_right] < DISTANCE_WALL

        enemy_behind = sensor_to_enemy[sensor_rear] < 0.1 or sensor_to_enemy[sensor_rear_left] < 0.1 or sensor_to_enemy[sensor_rear_right] < 0.1
        enemy_before = sensor_to_enemy[sensor_front] != 1.0 or sensor_to_enemy[sensor_front_left] != 1.0 or sensor_to_enemy[sensor_front_right] != 1.0

        ally_before = sensor_to_ally[sensor_front] != 1.0 or sensor_to_ally[sensor_front_left] != 1.0 or sensor_to_ally[sensor_front_right] != 1.0


        
        if (stuck_front + stuck_left + stuck_front_left) >= 2 or (stuck_front + stuck_front_right + stuck_right) >= 2:
            self.memory += 1
            translation = sensors[sensor_front]*0.3
            rotation = 0.6 * sensors[sensor_front_left] - 0.6 * sensors[sensor_front_right] + 0.6* sensors[sensor_left] - 0.6 * sensors[sensor_right] 
            return translation, rotation, False
        else :
            self.memory = 0

        if self.memory >= 15:
            translation = -0.3
            rotation = 0.1    
            return translation, rotation, False

        if self.robot_id == 3:
            param = [-0.8, -0.9, -0.1, -0.9, 0.4, 0.9, 0.5, -0.6]
            translation = math.tanh ( param[0] + param[1] * sensors[sensor_front_left] + param[2] * sensors[sensor_front] + param[3] * sensors[sensor_front_right] )
            rotation = math.tanh ( param[4] + param[5] * sensors[sensor_front_left] + param[6] * sensors[sensor_front] + param[7] * sensors[sensor_front_right] )
            return translation, rotation, False

        if enemy_behind:
            translation = 0
            rotation = -1.0 *sensor_to_enemy[sensor_rear_right] + 1.0 * sensor_to_enemy[sensor_rear_left]
            return translation, rotation, False
        
        if enemy_before:

            translation = sensor_to_enemy[sensor_front] *0.6 + sensor_to_enemy[sensor_front_left] * 0.4 + sensor_to_enemy[sensor_front_right] * 0.4
            rotation = 1.0 *sensor_to_enemy[sensor_front_right] -1.0 * sensor_to_enemy[sensor_front_left]
            return translation, rotation, False
        
        if ally_before:
            translation = 0.7 * sensors[sensor_front] 
            rotation = 1.0 *sensor_to_ally[sensor_front_right] -1.0 * sensor_to_ally[sensor_front_left] + 0.5 * (sensor_to_ally[sensor_front])
            return translation, rotation, False

    
        translation = sensors[sensor_front] * 0.6
        rotation = 0.5 * sensors[sensor_left] + 0.5 * sensors[sensor_front_left] - 0.5 * sensors[sensor_right] - 0.5 * sensors[sensor_front_right] + random.choice([-1,1]) * (1 - sensors[sensor_front])
        return translation, rotation, False



