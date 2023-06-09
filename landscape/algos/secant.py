import random

from domain.world import World
from domain.base_algo import BaseAlgo
import random


class Secant(BaseAlgo):
    f_min = None

    x_1 = None
    x_2 = None
    f_x_1 = None
    f_x_2 = None
    
    def get_next_iteration(self, world: World,f,df,ddf) -> float:
        # initialize search interval
        if world.tick_num == 0:
            self.x_1 = world.level.display_settings.origin.x
            self.x_2 = world.level.display_settings.origin.x + world.level.display_settings.sizex+0.9

            self.f_x_1 = f(self.x_1)
            self.f_x_2 = f(self.x_2)
            print("x1x2: {} {}".format(self.x_1,self.x_2))
            print("y1y2: {} {}".format(self.f_x_1,self.f_x_2))

        # every step building linear equation in form: slope * x + coef_k = y
        slope = (self.f_x_2-self.f_x_1)/(self.x_2-self.x_1)
        print("slope {}".format(slope))
        coef_k = self.f_x_1 - slope*self.x_1

        # new x is derived as solution to:  slope * x + coef_k = 0
        next_x = - coef_k/slope
        next_y = f(next_x)
        self.f_min = next_y

        # reassigning variables for next iteration
        self.f_x_1 = self.f_x_2
        self.x_1 = self.x_2
        self.f_x_2 = next_y
        self.x_2 = next_x

        return next_x
    
    def get_final_value(self):
        return self.f_min
