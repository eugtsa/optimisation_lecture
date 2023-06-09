from domain.world import World
from domain.base_algo import BaseAlgo
import random
import math


class Annealing(BaseAlgo):
    f_min = None
    t = 10
    
    def get_next_iteration(self, world: World,f,df,ddf) -> float:
        x = world.cur_pos
        
        left_display_bound = world.level.display_settings.origin.x
        right_display_bound = world.level.display_settings.origin.x+ world.level.display_settings.sizex

        # random jump point
        new_x = left_display_bound + random.random()*(right_display_bound-left_display_bound)

        # checking if we can jump there
        next_f_val = f(new_x)
        v_val = f(x)
        rand = random.random()
        try:
            if rand<math.exp(-(next_f_val-v_val)/self.t):
                # accepting
                self.f_min = next_f_val
                return new_x
            
            # rejecting
            return x
        finally:
            # cooling down
            self.t = self.t*0.8
    
    def get_final_value(self):
        return self.f_min
