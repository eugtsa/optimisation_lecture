import os
from domain.level import Level
from typing import List
import json


class LevelLoader:
    def list_levels(self) -> List[str]:
        return sorted([l for l in os.listdir("levels") if l.endswith("json")])

    def load_level(self, filename: str) -> Level:
        with open("levels" + os.sep + filename) as f:
            level_json = json.loads(f.read())

        return Level(level_json)
        
