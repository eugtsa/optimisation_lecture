from domain.world import World
from domain.action import Action


class BaseAlgo:
    def get_next_iteration(self, world: World) -> Action:
        raise NotImplementedError()
