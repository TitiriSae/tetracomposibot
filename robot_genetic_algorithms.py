
from robot import * 
import math
import numpy as np
import copy
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "Génétique"
    robot_id = -1
    iteration = 0
    param = []
    it_per_evaluation = 400
    trial = 0

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.mu = 5
        self.lambdaa = 20
        self.param_pere = [[random.randint(-1, 1) for i in range(8)] for j in range(self.mu)]
        self.param_fils = []
        self.param = []
        self.score = 0
        self.evaluations = evaluations
        self.it_per_evaluation = it_per_evaluation
        self.prec_translation = 0
        self.prec_rotation = 0
        super().__init__(x_0, y_0, theta_0, name=name, team=team)
         

    def reset(self):
        super().reset()
        self.param = self.mutation(self.param_pere[random.randint(0, self.mu-1)])


    def mutation(self, pere):
        fils = copy.deepcopy(pere)
        rand_idx = random.randint(0, len(pere)-1)

        poids = round(random.uniform(-1, 1), 1)

        fils[rand_idx] = poids
        return fils
    
    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")

        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        if self.iteration % self.it_per_evaluation == 0:

            
            if self.trial < self.evaluations:
                
                if self.iteration == 0:
                    print ("Trying strategy no.",self.trial)

                self.score += (self.log_sum_of_translation - self.prec_translation)*(1-abs(self.log_sum_of_rotation-self.prec_rotation))

                if self.param != []:
                    self.param_fils.append((self.param, self.score))
                    self.score = 0

                if len(self.param_fils) < self.lambdaa and len(self.param_fils) >= 5:
                    choix_pere = random.randint(0, self.mu-1)
                    self.param = self.mutation(self.param_pere[choix_pere])
                
                elif len(self.param_fils) < 5:
                    self.param = self.param_pere[len(self.param_fils)]

                else:
                    self.param_fils = sorted(self.param_fils, key=lambda x: x[1], reverse=True)
                    self.param_pere = [x[0] for x in self.param_fils[:5]]
                    self.trial = self.trial + 1
                    print ("Trying strategy no.",self.trial)
                    self.param_fils = []
                    self.reset()

                self.prec_translation = 0
                self.prec_rotation = 0
                self.iteration = self.iteration + 1
                return 0, 0, True # ask for reset

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )

        self.score += (self.log_sum_of_translation - self.prec_translation)*(1-abs(self.log_sum_of_rotation-self.prec_rotation))

        if self.trial >= self.evaluations:
            self.param = self.param_pere[0]
            print ("\tparameters           =",self.param)

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        self.iteration = self.iteration + 1   

        self.prec_translation = self.log_sum_of_translation
        self.prec_rotation = self.log_sum_of_rotation     

        return translation, rotation, False