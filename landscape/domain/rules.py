class Rules:
    def __init__(
        self, dot_score=10, move_score=-1, finish_score=20, hit_wall_score=-3
    ) -> None:
        self._dot_score = dot_score
        self._move_score = move_score
        self._finish_score = finish_score
        self._hit_wall_score = hit_wall_score

    @property
    def dot_score(self):
        return self._dot_score

    @property
    def move_score(self):
        return self._move_score

    @property
    def finish_score(self):
        return self._finish_score

    @property
    def hit_wall_score(self):
        return self._hit_wall_score
