from typing import List
from domain.target_function import TargetFunction, CompoundTargetFunction

from domain.display_settings import DisplaySettings


class Level:
    def __init__(
        self, level_json=None
    ) -> None:
        self._level_json = None
        self._display_settings = None
        self.target_function = None

        if level_json is not None:
            self._level_json = level_json
            self._set_target_function_from_json()
            self._read_display_settings_from_json()
            self.start_pos = self._level_json["start_pos"]


    def _set_target_function_from_json(self):
        subfunctions = list()
        
        for func_doc in self._level_json["target_function"]["subfunctions"]:
            new_tf = TargetFunction(
                func_doc["function"],
                func_doc["interval_start"],
                func_doc["interval_end"]
            )
            subfunctions.append(new_tf)

        self.target_function = CompoundTargetFunction()
        self.target_function.combine_tfs(*subfunctions)

    
    def _read_display_settings_from_json(self):
        self._display_settings = DisplaySettings(**self._level_json["display"])

    @property
    def display_settings(self):
        return self._display_settings
    
