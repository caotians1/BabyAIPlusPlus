from .dynamics_levels import DynamicsLevel
from babyai.levels.iclr19_levels import *


class Level_PutNextLocalDynamics_Lorem_Train(DynamicsLevel, Level_PutNextLocal):
    def __init__(self, seed=None):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)],
                               rand_text='lorem', instr_words=9, with_instruction=False)
        Level_PutNextLocal.__init__(self, room_size=8, num_objs=4, seed=seed)


class Level_PutNextLocalDynamics_Lorem_Fully_Train(DynamicsLevel, Level_PutNextLocal):
    def __init__(self, seed=None):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)],
                               rand_text='lorem', total_rand=True, instr_words=9, with_instruction=False)
        Level_PutNextLocal.__init__(self, room_size=8, num_objs=4, seed=seed)


class Level_PutNextLocalDynamics_Lorem_Test(DynamicsLevel, Level_PutNextLocal):
    def __init__(self, seed=None):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               rand_text='lorem', instr_words=9, with_instruction=False)
        Level_PutNextLocal.__init__(self, room_size=8, num_objs=4, seed=seed)


class Level_PutNextLocalDynamics_Lorem_Fully_Test(DynamicsLevel, Level_PutNextLocal):
    def __init__(self, seed=None):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               rand_text='lorem', instr_words=9, total_rand=True, with_instruction=False)
        Level_PutNextLocal.__init__(self, room_size=8, num_objs=4, seed=seed)


class Level_GoTo_NoDistDynamicsTrain(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 room_size=8,
                 num_rows=3,
                 num_cols=3,
                 doors_open=False,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)])
        Level_GoTo.__init__(self, room_size, num_rows, num_cols, 0, doors_open, seed)


class Level_GoTo_NoDistDynamicsTest(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 room_size=8,
                 num_rows=3,
                 num_cols=3,
                 doors_open=False,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2)
        Level_GoTo.__init__(self, room_size, num_rows, num_cols, 0, doors_open, seed)



class Level_GoTo2by2_PartialDynamics_Train(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 room_size=9,
                 num_rows=2,
                 num_cols=2,
                 num_dists=18,
                 doors_open=False,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[1, 2, 3, 4, 5],
                               n_floor_colors=3,
                               held_description=1,
                               held_out_cp_pairs=[('green', 1), ('red', 2), ('blue', 4)],
                               )
        Level_GoTo.__init__(self, room_size, num_rows,
                            num_cols, num_dists, doors_open, seed)


class Level_GoTo2by2_PartialDynamics_Test(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 room_size=9,
                 num_rows=2,
                 num_cols=2,
                 num_dists=18,
                 doors_open=False,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[1, 2, 3, 4, 5],
                               n_floor_colors=3,
                               held_description=1,
                               )

        Level_GoTo.__init__(self, room_size, num_rows,
                            num_cols, num_dists, doors_open, seed)


class Level_GoTo_RedBallDynamics_Lorem(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)],
                               rand_text='lorem', with_instruction=False)
        Level_GoToRedBallNoDists.__init__(self, seed)


class Level_GoTo_RedBallDynamics_Lorem_Fully(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)],
                               rand_text='lorem', total_rand=True, with_instruction=False)
        Level_GoToRedBallNoDists.__init__(self, seed)


class Level_GoTo_RedBallDynamicsSticky_Train(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 1)])
        Level_GoToRedBallNoDists.__init__(self, seed)


class Level_GoTo_RedBallDynamicsSticky_TargetPairOnly(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 4], n_floor_colors=2,
                               color_property_map={'green': ['trap'], 'blue': ['sticky']})
        Level_GoToRedBallNoDists.__init__(self, seed)


class Level_GoTo_RedBallDynamicsSticky_Test(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 4], n_floor_colors=2)
        Level_GoToRedBallNoDists.__init__(self, seed)


class Level_PutNextDynamics_Lorem_Train(DynamicsLevel, Level_PutNext):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)], with_instruction=with_instruction,
                               rand_text='lorem', total_rand=True)
        Level_PutNext.__init__(self, room_size=8, num_objs=4, seed=seed)


class Level_PutNextDynamics_Lorem_TargetPairOnly(DynamicsLevel, Level_PutNext):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               color_property_map={'green': ['trap', ],
                                                   'blue': ['slippery', ]}, with_instruction=with_instruction,
                               rand_text='lorem', total_rand=True,)
        Level_PutNext.__init__(self, room_size=8, num_objs=4, seed=seed)


class Level_PutNextDynamics_Lorem_Test(DynamicsLevel, Level_PutNext):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2, with_instruction=with_instruction,
                               rand_text='lorem', total_rand=True,)
        Level_PutNext.__init__(self, room_size=8, num_objs=4, seed=seed)


register_levels(__name__, {
                           'Level_GoTo_NoDistDynamicsTrain': Level_GoTo_NoDistDynamicsTrain,
                           'Level_GoTo_NoDistDynamicsTest': Level_GoTo_NoDistDynamicsTest,
                           'Level_GoTo2by2_PartialDynamics_Train': Level_GoTo2by2_PartialDynamics_Train,
                           'Level_GoTo2by2_PartialDynamics_Test': Level_GoTo2by2_PartialDynamics_Test,
                           'Level_GoTo_RedBallDynamics_Lorem': Level_GoTo_RedBallDynamics_Lorem,
                           'Level_GoTo_RedBallDynamics_Lorem_Fully': Level_GoTo_RedBallDynamics_Lorem_Fully,
                           'Level_GoTo_RedBallDynamicsSticky_Train': Level_GoTo_RedBallDynamicsSticky_Train,
                           'Level_GoTo_RedBallDynamicsSticky_TargetPairOnly': Level_GoTo_RedBallDynamicsSticky_TargetPairOnly,
                           'Level_GoTo_RedBallDynamicsSticky_Test': Level_GoTo_RedBallDynamicsSticky_Test,
                           'Level_PutNextLocalDynamics_Lorem_Train': Level_PutNextLocalDynamics_Lorem_Train,
                           'Level_PutNextLocalDynamics_Lorem_Fully_Train': Level_PutNextLocalDynamics_Lorem_Fully_Train,
                           'Level_PutNextLocalDynamics_Lorem_Test': Level_PutNextLocalDynamics_Lorem_Test,
                           'Level_PutNextLocalDynamics_Lorem_Fully_Test': Level_PutNextLocalDynamics_Lorem_Fully_Test,
                            'Level_PutNextDynamics_Lorem_Train':Level_PutNextDynamics_Lorem_Train,
                            'Level_PutNextDynamics_Lorem_TargetPairOnly':Level_PutNextDynamics_Lorem_TargetPairOnly,
                            'Level_PutNextDynamics_Lorem_Test':Level_PutNextDynamics_Lorem_Test,
                           })