from domain.world import World
from domain.base_algo import BaseAlgo
from helpers.helpers import BinaryGenetics
import struct
import math
import random
import numpy as np
import logging


def gen_initial_samples_from_numbers(list_of_floats):
    samples = np.zeros((len(list_of_floats),32))
    for i,num in enumerate(list_of_floats):
        samples[i,:] = float_to_bits(num)
    return samples


def bits_to_float(bits):
    value = int(''.join('1' if b else '0' for b in bits) , 2)
    my_bytes = value.to_bytes(4, byteorder='little')
    returned = struct.unpack('f',my_bytes)
    if math.isnan(returned[0]):
        return 0.0
    if returned[0] == float('inf'):
        return 0.1
    return returned[0]


def float_to_bits(f_num):
    num_bytes_as_bools = struct.pack('f',f_num)
    num_as_int = struct.unpack('i',num_bytes_as_bools)
    leftovers = num_as_int[0]
    my_byte = list()
    for i in range(31,-1,-1):
        byte_i,leftovers = divmod(leftovers,2**i)
        my_byte.append(byte_i)
    return my_byte


class Genetic(BaseAlgo):
    f_min = None
    bg = None
    genetic_iterator = None

    
    
    def get_next_iteration(self, world: World,f,df,ddf) -> float:
        if world.tick_num == 0:
            left_display_bound = world.level.display_settings.origin.x
            right_display_bound = world.level.display_settings.origin.x+ world.level.display_settings.sizex
            span = right_display_bound-left_display_bound

            n_samples = 20
            random_nums = [left_display_bound+random.random()*span for _ in range(n_samples)]
            initial_samples = gen_initial_samples_from_numbers(random_nums)

            self.bg = BinaryGenetics(n_generations=51,
                    n_samples = n_samples,
                    save_best_n = 1,
                    binary_shape=32, # 32 bit float, one parameter
                    logging_obj= None,
                    p_point_mutate=0.1,
                    tournament_rounds = 2,
                    random_interchange_prob = 0.1,
                    inbreed_prob=0.1,
                    tqdm_obj=lambda x: x)
            
            eval_func = lambda x: f(bits_to_float(x))

            self.bg.set_eval_func(eval_func, greater_is_better=False)
            self.genetic_iterator = iter(self.bg.learn(yield_best=True,samples=initial_samples))
        
        res = self.genetic_iterator.__next__()
    
        best_vec = res[0]
        best_result = res[1]

        x = bits_to_float(best_vec)
        self.f_min = f(x)
        return x
    
    def get_final_value(self):
        return self.f_min
