import random

from domain.world import World
from domain.base_algo import BaseAlgo
import random


class Golden(BaseAlgo):
    f_min = None

    x_l = None
    x_h = None
    x_a = None
    x_b = None
    f_x_l = None
    f_x_h = None
    f_x_a = None
    f_x_b = None
    phi = (1.0 + 5.0 ** 0.5) / 2.0
    
    def get_next_iteration(self, world: World,f,df,ddf) -> float:
        # initialize search interval
        if world.tick_num == 0:
            self.x_l = world.level.display_settings.origin.x
            self.x_h = world.level.display_settings.origin.x + world.level.display_settings.sizex
            self.x_a = self.x_h-(self.x_h-self.x_l)/self.phi

            self.f_x_l = f(self.x_l)
            self.f_x_h = f(self.x_h)
            self.f_x_a = f(self.x_a)

        # every step calculating target function f only once!
        if self.x_a is None:
            self.x_a = self.x_h-(self.x_h-self.x_l)/self.phi
            self.f_x_a = f(self.x_a)
            self.f_min = self.f_x_a
            next_x = self.x_a
        else:
            self.x_b = self.x_l+(self.x_h-self.x_l)/self.phi
            self.f_x_b = f(self.x_b)
            self.f_min = self.f_x_b
            next_x = self.x_b

        # reassinning two other points
        if self.f_x_b<self.f_x_a:
            self.x_l = self.x_a
            self.f_x_l = self.f_x_a
            self.x_a = self.x_b
            self.f_x_a = self.f_x_b
            self.x_b = None
        else:
            self.x_h = self.x_b
            self.f_x_h = self.f_x_b
            self.x_b = self.x_a
            self.f_x_b = self.f_x_a
            self.x_a = None

        return next_x
    
    def get_final_value(self):
        return self.f_min
