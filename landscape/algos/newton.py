from domain.world import World
from domain.base_algo import BaseAlgo
import math


class Newton(BaseAlgo):
    f_min = None
    
    def get_next_iteration(self, world: World,f,df,ddf) -> float:
        x = world.cur_pos
        x_next = x-df(x)/ddf(x)
        self.f_min = f(x_next)
        return x_next
    
    def get_final_value(self):
        return self.f_min
