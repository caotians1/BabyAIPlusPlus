import gym
from babyai.levels.verifier import *
from babyai.levels.levelgen import register_levels
from babyai.levels.iclr19_levels import Level_GoTo
from .decriptive_level_base import DescriptiveLevel
from .dynamics_levels import DynamicsLevel

class Level_GoTo_Desc(DescriptiveLevel, Level_GoTo):
    def __init__(self,
                 room_size=8,
                 num_rows=3,
                 num_cols=3,
                 num_dists=18,
                 doors_open=False,
                 seed=None
                 ):

        DescriptiveLevel.__init__(self, 1, 1.0)
        Level_GoTo.__init__(self, room_size, num_rows, num_cols, num_dists, doors_open, seed)

class Level_GoTo_DescDynamic(DescriptiveLevel, DynamicsLevel, Level_GoTo):
    def __init__(self,
                 room_size=8,
                 num_rows=3,
                 num_cols=3,
                 num_dists=18,
                 doors_open=False,
                 seed=None):
        DynamicsLevel.__init__(self, [1, 3, 5], 3, seed, 1, 1.0, room_size, num_rows, num_cols, num_dists, doors_open, seed)


register_levels(__name__, {'Level_GoTo_Desc':Level_GoTo_Desc, 'Level_GoTo_DescDynamic':Level_GoTo_DescDynamic})
