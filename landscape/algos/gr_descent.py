from domain.world import World
from domain.base_algo import BaseAlgo


class GrDescent(BaseAlgo):
    f_min = None
    alpha = 0.023
    
    def get_next_iteration(self, world: World,f,df,ddf) -> float:
        x = world.cur_pos
        x_next = x-df(x)*self.alpha
        self.f_min = f(x_next)
        return x_next
    
    def get_final_value(self):
        return self.f_min
