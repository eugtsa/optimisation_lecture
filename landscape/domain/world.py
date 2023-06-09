from domain.level import Level
from domain.action import Action
from typing import Set


class World:
    def __init__(
        self,
        level: Level,
        cur_pos: float,
        cur_score: float,
        tick_num: int = 0,
    ) -> None:
        self._level = level
        self._cur_pos = cur_pos
        self._cur_score = cur_score
        self._tick_num = tick_num
        self.best_x = None
        self.best_f = None

    def update_cur_pos(self, new_pos):
        self._cur_pos = new_pos

    def to_pixel_coords(self, x, y):
        return \
            int((x-self._level.display_settings.origin.x)*self._level.display_settings.pixels_in_one_x_scale),\
            int((-float(y)+self._level.display_settings.sizey+self._level.display_settings.origin.y)*self._level.display_settings.pixels_in_one_x_scale)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self,new_level):
        self._level = new_level

    @property
    def tick_num(self):
        return self._tick_num
    
    @tick_num.setter
    def tick_num(self, new_tick):
        self._tick_num = new_tick

    @property
    def score(self):
        return self._cur_score
    
    @score.setter
    def score(self,new_score):
        self._cur_score = new_score

    @property
    def cur_pos(self):
        return self._cur_pos

    def is_finished(self):
        return self.tick_num>50