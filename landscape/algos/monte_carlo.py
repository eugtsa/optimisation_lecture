import random

from domain.world import World
from domain.base_algo import BaseAlgo
import random


class MonteCarlo(BaseAlgo):
    f_min = None
    def get_next_iteration(self, world: World,f,df,ddf) -> float:
        left_display_bound = world.level.display_settings.origin.x
        right_display_bound = world.level.display_settings.origin.x+ world.level.display_settings.sizex

        new_x = left_display_bound + random.random()*(right_display_bound-left_display_bound)
        f_val = f(new_x)

        if self.f_min is None:
            self.f_min = f_val
        elif f_val<self.f_min:
            self.f_min = f_val
        return new_x
    
    def get_final_value(self):
        return self.f_min
