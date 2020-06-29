import gym
from babyai.levels.verifier import *
from babyai.levels.levelgen import *
from babyai.levels.iclr19_levels import *
from gym_minigrid.minigrid import COLOR_NAMES, Floor, DIR_TO_VEC
from lorem.text import TextLorem

PROPERTY_TO_IDX = {
    'trap': 0,  # Agent dies, episode end
    'sticky': 1,  # Agent must stay on block for at least 3 time steps.
    'flipud': 2,  # causes agent to turn 180 and move one block, requires agent to spin and then getting backed out.
    'fliplr': 3,  # Flips rotational actions.
    'slippery': 4,  # time warp, increase reward at end
    # Agent will fall down 1 block every 2 timesteps on this color.
    'magic': 5,
}

PROPERTY_ORDER = [['trap'], ['slippery', 'magic'], ['none', 'sticky', 'flipud', 'fliplr']]
Spawn_rates = [0.05, 0.15, 0.30]
N_tries = 20
"""
property game breaking levels:
1. unconstrained: can be placed anywhere without breaking game
2. path blocking: creates uncrossable areas, must be placed not infront of doors, must not be contiguous with other path blockers by more than 2
3. insta-death: path-blocking + must not overlap with object. 
property rarity:
1. unconstrained are common: 30% spawn chance
2. path blocking are rare: 15% spawn
3. insta-death super rare: 5% spawn
"""

IDX_TO_PROPERTY = dict(zip(PROPERTY_TO_IDX.values(), PROPERTY_TO_IDX.keys()))


class DynamicsLevel(RoomGridLevel):
    # TODO(lts): Adapted floors to be containers. Need to make sure certain objectives will continue
    # to work. (Current goto objective should work b/c colored floors never spawn under objects.)
    def __init__(self, enabled_properties=(0, 1, 2, 3, 4, 5), n_floor_colors=2, fixed_color_prop_map=False,
                 color_property_map=None, held_out_cp_pairs=None, held_description=0.0, with_instruction=True,
                 rand_text=False, total_rand=False, instr_words=5,
                 *args, **kwargs):
        """
                Render this grid at a given scale
        :param enabled_properties: list of property idxs that are enabled.
        :param n_floor_colors: number of colors for special floors.
        :param fixed_color_prop_map: always use the same color prop map, default False
        :param color_property_map: use this color prop map, default None (generate random color prop map)
        :param held_out_cp_pairs: use this to prevent certain prop maps from showing up
        :param held_description: fractional chance of description of a color property pair being withheld
        :param with_instruction: Include instruction of the task
        :param rand_text: If 'rand_attribute', randomize the color-property maps: If True, replace description with
                          meaningless text.
        :param total_rand: replace description with meaningless text coming from a large dictionary
        :param instr_words: number of words in the instruction (only used for generating random text)
        :param args:
        :param kwargs:
        """
        assert n_floor_colors <= len(COLOR_NAMES)
        assert len(enabled_properties) > 0
        assert max(enabled_properties) < len(PROPERTY_TO_IDX)
        assert min(enabled_properties) >= 0

        self.enabled_properties = enabled_properties
        self.n_floor_colors = n_floor_colors
        self.held_out_cp_pairs = held_out_cp_pairs
        self.desc = ''
        self.fixed_color_prop_map = fixed_color_prop_map
        if color_property_map is None:
            self.color_property_map = {}
            self.color_property_map_fixed = {}
        else:
            self.color_property_map = {} #color_property_map
            self.color_property_map_fixed = color_property_map.copy()
            self.fixed_color_prop_map = True
        self.held_description = held_description
        # Properties for tile effects.
        self.tile_time = 0
        self.last_color = None
        self.color_time = 0
        self.agent_prev_pos = None
        self.with_instruction = with_instruction
        self.rand_text = rand_text
        self.total_rand = total_rand
        self.instr_words = instr_words
        super().__init__(*args, **kwargs)

    def gen_mission(self):
        # TODO(lts)
        super().gen_mission()

        return

    def reset(self, **kwargs):

        self.tile_time = 0
        self.last_color = None
        self.color_time = 0
        self.agent_prev_pos = None

        # Rescramble floor property mappings.
        # TODO(lts): Hold some out for test.
        if len(self.color_property_map_fixed) > 0 and self.fixed_color_prop_map:
            # determine which colors are to be used
            self.color_property_map = {}
            color_keys = [c for c in self.color_property_map_fixed.keys()]
            inds = np.arange(len(color_keys))
            self.np_random.shuffle(inds)
            assert len(inds) >= self.n_floor_colors
            inds = inds[:self.n_floor_colors]
            for i in inds:
                c = color_keys[i]
                self.color_property_map[c] = random.choice(self.color_property_map_fixed[c])
            # for count, c in enumerate(self.color_property_map_fixed.keys()):
            #     self.color_property_map[c] = random.choice(self.color_property_map_fixed[c])
            # print ("color_maps", self.color_property_map, self.color_property_map_fixed)
        else:
            self.color_property_map = {}
            for i in range(self.n_floor_colors):
                # Random property per color. Can have duplicates.
                if self.held_out_cp_pairs is not None:
                    if type(self.held_out_cp_pairs[0][0]) == str:
                        c = COLOR_NAMES[i]
                    else:
                        c = i
                    # print (c, self.held_out_cp_pairs)
                    held_out_cs = []
                    for c, p in self.held_out_cp_pairs:
                        if c == COLOR_NAMES[i]:
                            held_out_cs.append(p)
                    # held_out_cs = [c for c, p in self.held_out_cp_pairs]
                    # print ("held_out_cs", held_out_cs)
                    # if c in held_out_cs:
                    enabled_properties = self.enabled_properties.copy()

                    for c in held_out_cs:
                        # print (enabled_properties, held_out_cs, c, held_out_cs.index(c))
                        # enabled_properties.pop(held_out_cs.index(c))
                        enabled_properties.remove(c)
                        # print (enabled_properties)
                        rand_property_idx = enabled_properties[self._rand_int(
                            0, len(enabled_properties))]

                    if held_out_cs == []:
                        rand_property_idx = self.enabled_properties[self._rand_int(
                            0, len(self.enabled_properties))]
                else:
                    rand_property_idx = self.enabled_properties[self._rand_int(
                        0, len(self.enabled_properties))]
                self.color_property_map[COLOR_NAMES[i]] = IDX_TO_PROPERTY[rand_property_idx]
                # print ("color_map", self.color_property_map)

        # print(self.color_property_map)
        obs = super().reset()
        self.desc = '. '
        if self.held_description == 0:
            items = list(self.color_property_map.items())
        else:
            N = len(self.color_property_map)
            assert self.held_description <= N
            inc = N - self.held_description
            items = list(self.color_property_map.items())
            random.shuffle(items)
            items = items[:inc]
        if not self.rand_text:
            for color, prop in items:
                self.desc += '%s floors are %s. ' % (color, prop)
        elif self.rand_text == "rand_attribute":
            props = list(PROPERTY_TO_IDX.keys())
            for color, prop in items:
                self.desc += '%s floors are %s' % (self._rand_color(), props[self._rand_int(0, len(prop))])
        else:
            # separate words by '-'
            # sentence length should be between 2 and 3
            # choose words from A, B, C and D
            if self.total_rand:
                lorem = TextLorem(srange=(self.instr_words, self.instr_words))
                self.desc += lorem.sentence()
                lorem = TextLorem(srange=(4, 4))
            else:
                lorem = TextLorem(srange=(self.instr_words, self.instr_words),
                                  words=['put', 'the', 'ball', 'in', 'lorem', 'ipsum', 'forty-two', 'sentence',
                                         'length', 'agent', 'dir', 'gen', 'grid', 'word', 'description', 'choose',
                                         'previous'])
                self.desc += lorem.sentence()
                lorem = TextLorem(srange=(4, 4),
                                  words=['put', 'the', 'ball', 'in', 'lorem', 'ipsum', 'forty-two', 'sentence',
                                         'length', 'agent', 'dir', 'gen', 'grid', 'word', 'description', 'choose',
                                         'previous'])

            for color, prop in items:
                self.desc += ' ' + lorem.sentence()

        if self.with_instruction:
            obs['mission'] += self.desc
        else:
            obs['mission'] = self.desc[2:]
        return obs

    def _gen_grid(self, width, height):
        super()._gen_grid(width, height)

        self.previous_direction = self.agent_dir
        # Randomly place some colored floor tiles.
        cmap = self.color_property_map

        contig_colors = []
        level_0_cp = [(p, c) for c, p in cmap.items() if p in PROPERTY_ORDER[0]]
        contig_colors.extend(c for p, c in level_0_cp)
        n_color_0 = len(level_0_cp)
        # level 1
        level_1_cp = [(p, c) for c, p in cmap.items() if p in PROPERTY_ORDER[1]]
        contig_colors.extend(c for p, c in level_1_cp)
        n_color_1 = len(level_1_cp)
        # level 2
        level_2_cp = [(p, c) for c, p in cmap.items() if p in PROPERTY_ORDER[2]]
        n_color_2 = len(level_2_cp)

        for i in range(self.num_cols * self.num_rows * pow(self.room_size - 2, 2)):
            f = self._rand_float(0, 1)
            if f >= 1 - Spawn_rates[0] and n_color_0 > 0:
                c = self._rand_int(0, n_color_0)
                i = self._rand_int(0, self.num_cols)
                j = self._rand_int(0, self.num_rows)
                try:
                    for _ in range(N_tries):
                        obj, pose = self.place_in_room(i, j, Floor(level_0_cp[c][1]))
                        room = self.get_room(i, j)
                        offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
                        flag = 0
                        for offset in offsets:
                            n_pose = pose + offset
                            tar = self.grid.get(*n_pose)
                            if tar is not None:
                                # check contiguous
                                if tar.type is 'floor' and tar.color in contig_colors:
                                    flag += 1
                                # check door
                                elif tar.type is 'door':
                                    flag += 2
                        if flag > 1:
                            # revert
                            self.grid.set(pose[0], pose[1], None)
                            room.objs.pop(-1)
                        else:
                            # succesfully placed floor
                            break
                except RecursionError:
                    print("room %d %d too full" % (i, j))
                    continue
            elif f >= 1 - sum(Spawn_rates[:2]) and n_color_1 > 0:
                c = self._rand_int(0, n_color_1)
                i = self._rand_int(0, self.num_cols)
                j = self._rand_int(0, self.num_rows)
                try:
                    for _ in range(N_tries):
                        obj, pose = self.place_in_room(i, j, Floor(level_1_cp[c][1]))
                        room = self.get_room(i, j)
                        offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
                        flag = 0
                        for offset in offsets:
                            n_pose = pose + offset
                            tar = self.grid.get(*n_pose)
                            if tar is not None:
                                # check contiguous
                                if tar.type is 'floor' and tar.color in contig_colors:
                                    flag += 1
                                # check door
                                elif tar.type is 'door':
                                    flag += 2
                        if flag > 1:
                            # revert
                            self.grid.set(pose[0], pose[1], None)
                            room.objs.pop(-1)
                        else:
                            # succesfully placed floor
                            break
                except RecursionError:
                    print("room %d %d too full" % (i, j))
                    continue

            elif f >= 1 - sum(Spawn_rates[:3]) and n_color_2 > 0:
                c = self._rand_int(0, n_color_2)
                i = self._rand_int(0, self.num_cols)
                j = self._rand_int(0, self.num_rows)
                try:
                    self.place_in_room(i, j, Floor(level_2_cp[c][1]))
                except RecursionError:
                    print("room %d %d too full" % (i, j))
                    continue

    def get_floor_color(self, i, j):
        o = self.grid.get(i, j)
        if o and o.type == 'floor':
            return o.color
        return None

    @property
    def down_pos(self):
        """
        Get the position of the cell that is one cell below agent.
        """

        return self.agent_pos + DIR_TO_VEC[1]

    def step(self, action):
        c = self.get_floor_color(*self.agent_pos)
        # Deal with different floor tiles.
        floor_property = None
        if c:
            floor_property = self.color_property_map[c]

        if floor_property == 'fliplr':
            if action == self.actions.left:
                action = self.actions.right
            elif action == self.actions.right:
                action = self.actions.left
        elif floor_property == 'flipud':
            if action == self.actions.forward:
                self.agent_dir = (self.agent_dir + 2) % 4
        elif floor_property == 'sticky':
            if self.tile_time < 2 and action == self.actions.forward:
                action = self.actions.done  # Wait action.
        elif floor_property == "slippery":
            self.step_count -= 0.5
        elif floor_property == 'magic':
            if self.color_time > 0 and self.color_time % 2:
                down_cell = self.grid.get(*self.down_pos)
                # Move Agent down.
                if down_cell == None or down_cell.can_overlap():
                    self.agent_pos = self.down_pos
                    # TODO(lts): Allow instructions to be finished via gravity.

        self.agent_prev_pos = self.agent_pos

        # Actually take action
        obs, reward, done, info = super().step(action)
        c = self.get_floor_color(*self.agent_pos)
        if c:
            floor_property = self.color_property_map[c]
        if floor_property == "trap":
            reward = 0
            done = True

        # Keep track of some internal variables.
        # Previous Location
        if not np.array_equal(self.agent_prev_pos, self.agent_pos):
            self.tile_time = 0
        else:
            self.tile_time += 1

        # Previous color
        if (self.last_color != self.agent_pos).all():
            #self.last_color = self.get_floor_color(*self.agent_pos)
            self.last_color = self.agent_pos
            self.color_time = 0
        else:
            self.color_time += 1
        if self.with_instruction:
            obs['mission'] += self.desc
        else:
            obs['mission'] = self.desc[2:]

        return obs, reward, done, info


# Goto Red ball Dynamic
class Level_GoTo_RedBallDynamics_Train(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None,
                 with_instruction=True,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)], with_instruction=with_instruction)
        Level_GoToRedBallNoDists.__init__(self, seed)


class Level_GoTo_RedBallDynamics_TargetPairOnly(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None,
                 with_instruction=True,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               color_property_map={'green': ['trap'], 'blue': ['slippery']},
                               with_instruction=with_instruction)
        Level_GoToRedBallNoDists.__init__(self, seed)


class Level_GoTo_RedBallDynamics_Test(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None,
                 with_instruction=True,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2, with_instruction=with_instruction)
        Level_GoToRedBallNoDists.__init__(self, seed)

register_levels(__name__, {'Level_GoTo_RedBallDynamics_Train': Level_GoTo_RedBallDynamics_Train,
                           'Level_GoTo_RedBallDynamics_TargetPairOnly': Level_GoTo_RedBallDynamics_TargetPairOnly,
                           'Level_GoTo_RedBallDynamics_Test': Level_GoTo_RedBallDynamics_Test
                           })

# Goto Red ball dynamic hard
class Level_GoTo_RedBallDynamics_Hard_Train(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None,
                 with_instruction=True,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               held_out_cp_pairs=[('green', 0), ('green', 2),
                                                  ('grey', 3), ('grey', 4),
                                                  ('blue', 1), ('blue', 5)], with_instruction=with_instruction, )
        Level_GoToRedBallNoDists.__init__(self, seed)


class Level_GoTo_RedBallDynamics_Hard_TargetPairOnly(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None,
                 with_instruction=True,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['trap', 'flipud'],
                                                   'grey': ['fliplr', 'slippery'],
                                                   'blue': ['sticky', 'magic']}, with_instruction=with_instruction, )
        Level_GoToRedBallNoDists.__init__(self, seed)


class Level_GoTo_RedBallDynamics_Hard_Test(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None,
                 with_instruction=True,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               with_instruction=with_instruction, )
        Level_GoToRedBallNoDists.__init__(self, seed)

class Level_GoTo_RedBallDynamics_Hard_Fixed(DynamicsLevel, Level_GoToRedBallNoDists):
    def __init__(self,
                 seed=None,
                 with_instruction=True,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['slippery', ],
                                                   'grey': ['flipud'],
                                                   'blue': ['fliplr'],
                                                   'red': ['trap'],
                                                   'purple': ['magic'],
                                                   'yellow': ['sticky'],
                                                   },
                               with_instruction=with_instruction, )
        Level_GoToRedBallNoDists.__init__(self, seed)

register_levels(__name__, {'Level_GoTo_RedBallDynamics_Hard_Train': Level_GoTo_RedBallDynamics_Hard_Train,
                           'Level_GoTo_RedBallDynamics_Hard_TargetPairOnly': Level_GoTo_RedBallDynamics_Hard_TargetPairOnly,
                           'Level_GoTo_RedBallDynamics_Hard_Test': Level_GoTo_RedBallDynamics_Hard_Test,
                           'Level_GoTo_RedBallDynamics_Hard_Fixed':Level_GoTo_RedBallDynamics_Hard_Fixed
                           })
# Goto Redball dynamic maze

class Level_GoToRedBall_Maze(RoomGridLevel):
    """
    Go to the red ball, 3x3 rooms, without distractors.
    """

    def __init__(self, seed=None):
        super().__init__(
            num_rows=3,
            num_cols=3,
            room_size=8,
            seed=seed
        )

    def gen_mission(self):
        self.place_agent()
        self.connect_all()
        i = self.np_random.randint(3)
        j = self.np_random.randint(3)
        obj, _ = self.add_object(i, j, 'ball', 'red')

        # Make sure no unblocking is required
        self.check_objs_reachable()

        self.instrs = GoToInstr(ObjDesc(obj.type, obj.color))


class Level_GoTo_RedBallDynamics_Maze_Train(DynamicsLevel, Level_GoToRedBall_Maze):
    def __init__(self,
                 seed=None,
                 with_instruction=True,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               held_out_cp_pairs=[('green', 0), ('green', 2),
                                                  ('grey', 3), ('grey', 4),
                                                  ('blue', 1), ('blue', 5)], with_instruction=with_instruction, )
        Level_GoToRedBall_Maze.__init__(self, seed)


class Level_GoTo_RedBallDynamics_Maze_TargetPairOnly(DynamicsLevel, Level_GoToRedBall_Maze):
    def __init__(self,
                 seed=None,
                 with_instruction=True,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['trap', 'flipud'],
                                                   'grey': ['fliplr', 'slippery'],
                                                   'blue': ['sticky', 'magic']}, with_instruction=with_instruction, )
        Level_GoToRedBall_Maze.__init__(self, seed)


class Level_GoTo_RedBallDynamics_Maze_Test(DynamicsLevel, Level_GoToRedBall_Maze):
    def __init__(self,
                 seed=None,
                 with_instruction=True,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               with_instruction=with_instruction, )
        Level_GoToRedBall_Maze.__init__(self, seed)


class Level_GoTo_RedBallDynamics_Maze_Fixed(DynamicsLevel, Level_GoToRedBall_Maze):
    def __init__(self,
                 seed=None,
                 with_instruction=True,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['slippery', ],
                                                   'grey': ['flipud'],
                                                   'blue': ['fliplr'],
                                                   'red': ['trap'],
                                                   'purple': ['magic'],
                                                   'yellow': ['sticky'],
                                                   },
                               with_instruction=with_instruction, )
        Level_GoToRedBall_Maze.__init__(self, seed)


register_levels(__name__, {'Level_GoTo_RedBallDynamics_Maze_Train': Level_GoTo_RedBallDynamics_Maze_Train,
                           'Level_GoTo_RedBallDynamics_Maze_TargetPairOnly': Level_GoTo_RedBallDynamics_Maze_TargetPairOnly,
                           'Level_GoTo_RedBallDynamics_Maze_Test': Level_GoTo_RedBallDynamics_Maze_Test,
                           'Level_GoTo_RedBallDynamics_Maze_Fixed':Level_GoTo_RedBallDynamics_Maze_Fixed
                           })
# Put Next Local Dynamic

class Level_PutNextLocalDynamics_Train(DynamicsLevel, Level_PutNextLocal):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)], with_instruction=with_instruction)
        Level_PutNextLocal.__init__(self, room_size=8, num_objs=4, seed=seed)


class Level_PutNextLocalDynamics_TargetPairOnly(DynamicsLevel, Level_PutNextLocal):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               color_property_map={'green': ['trap', ],
                                                   'blue': ['slippery', ]}, with_instruction=with_instruction)
        Level_PutNextLocal.__init__(self, room_size=8, num_objs=4, seed=seed)


class Level_PutNextLocalDynamics_Test(DynamicsLevel, Level_PutNextLocal):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2, with_instruction=with_instruction)
        Level_PutNextLocal.__init__(self, room_size=8, num_objs=4, seed=seed)

class Level_PutNextLocalDynamics_Fixed(DynamicsLevel, Level_PutNextLocal):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               color_property_map={'green': ['slippery', ],
                                                   'red': ['trap'],
                                                   'yellow': ['sticky'],
                                                   },
                               with_instruction=with_instruction)
        Level_PutNextLocal.__init__(self, room_size=8, num_objs=4, seed=seed)

register_levels(__name__, {'Level_PutNextLocalDynamics_Train': Level_PutNextLocalDynamics_Train,
                           'Level_PutNextLocalDynamics_TargetPairOnly': Level_PutNextLocalDynamics_TargetPairOnly,
                           'Level_PutNextLocalDynamics_Test': Level_PutNextLocalDynamics_Test,
                           'Level_PutNextLocalDynamics_Fixed': Level_PutNextLocalDynamics_Fixed
                           })
# Put Next to Dynamic

class Level_PutNextDynamics_Train(DynamicsLevel, Level_PutNext):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)], with_instruction=with_instruction)
        Level_PutNext.__init__(self, room_size=8, seed=seed)


class Level_PutNextDynamics_TargetPairOnly(DynamicsLevel, Level_PutNext):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               color_property_map={'green': ['trap', ],
                                                   'blue': ['slippery', ]}, with_instruction=with_instruction)
        Level_PutNext.__init__(self, room_size=8, seed=seed)


class Level_PutNextDynamics_Test(DynamicsLevel, Level_PutNext):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2, with_instruction=with_instruction)
        Level_PutNext.__init__(self, room_size=8, seed=seed)

register_levels(__name__, {'Level_PutNextDynamics_Train': Level_PutNextDynamics_Train,
                           'Level_PutNextDynamics_TargetPairOnly': Level_PutNextDynamics_TargetPairOnly,
                           'Level_PutNextDynamics_Test': Level_PutNextDynamics_Test,
                           })
#  Put Next to Dynamic Hard

class Level_PutNextDynamics_Hard_Train(DynamicsLevel, Level_PutNext):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               held_out_cp_pairs=[('green', 0), ('green', 2),
                                                  ('grey', 3), ('grey', 4),
                                                  ('blue', 1), ('blue', 5)], with_instruction=with_instruction, )
        Level_PutNext.__init__(self, room_size=8, seed=seed)


class Level_PutNextDynamics_Hard_TargetPairOnly(DynamicsLevel, Level_PutNext):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['trap', 'flipud'],
                                                   'grey': ['fliplr', 'slippery'],
                                                   'blue': ['sticky', 'magic']}, with_instruction=with_instruction,)
        Level_PutNext.__init__(self, room_size=8, seed=seed)


class Level_PutNextDynamics_Hard_Test(DynamicsLevel, Level_PutNext):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               with_instruction=with_instruction, )
        Level_PutNext.__init__(self, room_size=8, seed=seed)

register_levels(__name__, {'Level_PutNextDynamics_Hard_Train': Level_PutNextDynamics_Hard_Train,
                           'Level_PutNextDynamics_Hard_TargetPairOnly': Level_PutNextDynamics_Hard_TargetPairOnly,
                           'Level_PutNextDynamics_Hard_Test': Level_PutNextDynamics_Hard_Test,
                           })

# Goto Maze Dynamic
class Level_GoToObjMaze_Dynamics_Train(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               held_out_cp_pairs=[('green', 0), ('green', 2),
                                                  ('grey', 3), ('grey', 4),
                                                  ('blue', 1), ('blue', 5)], with_instruction=with_instruction)
        Level_GoTo.__init__(self, room_size=11, num_rows=3, num_dists=1,
                            num_cols=3, doors_open=False, seed=seed)

class Level_GoToObjMaze_Dynamics_TargetPairOnly(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['trap', 'flipud'],
                                                   'grey': ['fliplr', 'slippery'],
                                                   'blue': ['sticky', 'magic']}, with_instruction=with_instruction)
        Level_GoTo.__init__(self, room_size=11, num_rows=3, num_dists=1,
                            num_cols=3, doors_open=False, seed=seed)

class Level_GoToObjMaze_Dynamics_Test(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               with_instruction=with_instruction)
        Level_GoTo.__init__(self, room_size=11, num_rows=3, num_dists=1,
                            num_cols=3, doors_open=False, seed=seed)

register_levels(__name__, {'Level_GoToObjMaze_Dynamics_Train': Level_GoToObjMaze_Dynamics_Train,
                           'Level_GoToObjMaze_Dynamics_TargetPairOnly': Level_GoToObjMaze_Dynamics_TargetPairOnly,
                           'Level_GoToObjMaze_Dynamics_Test': Level_GoToObjMaze_Dynamics_Test,
                           })


# Goto local Dynamic

class Level_GoToLocal_Dynamics_Train(DynamicsLevel, Level_GoToLocal):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)], with_instruction=with_instruction)
        Level_GoToLocal.__init__(self, room_size=11, num_dists=8, seed=seed)

class Level_GoToLocal_Dynamics_TargetPairOnly(DynamicsLevel, Level_GoToLocal):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               color_property_map={'green': ['trap', ],
                                                   'blue': ['slippery', ]}, with_instruction=with_instruction)
        Level_GoToLocal.__init__(self, room_size=11, num_dists=8, seed=seed)

class Level_GoToLocal_Dynamics_Test(DynamicsLevel, Level_GoToLocal):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               with_instruction=with_instruction)
        Level_GoToLocal.__init__(self, room_size=11, num_dists=8, seed=seed)

register_levels(__name__, {'Level_GoToLocal_Dynamics_Train': Level_GoToLocal_Dynamics_Train,
                           'Level_GoToLocal_Dynamics_TargetPairOnly': Level_GoToLocal_Dynamics_TargetPairOnly,
                           'Level_GoToLocal_Dynamics_Test': Level_GoToLocal_Dynamics_Test,
                           })

# Goto Dynamic

class Level_GoTo_Dynamics_Train(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)], with_instruction=with_instruction)
        Level_GoTo.__init__(self, room_size=11, num_rows=3, num_dists=11,
                            num_cols=3, doors_open=False, seed=seed)

class Level_GoTo_Dynamics_TargetPairOnly(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               color_property_map={'green': ['trap', ],
                                                   'blue': ['slippery', ]}, with_instruction=with_instruction)
        Level_GoTo.__init__(self, room_size=11, num_rows=3, num_dists=11,
                            num_cols=3, doors_open=False, seed=seed)

class Level_GoTo_Dynamics_Test(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               with_instruction=with_instruction)
        Level_GoTo.__init__(self, room_size=11, num_rows=3, num_dists=11,
                            num_cols=3, doors_open=False, seed=seed)


register_levels(__name__, {'Level_GoTo_Dynamics_Train': Level_GoTo_Dynamics_Train,
                           'Level_GoTo_Dynamics_TargetPairOnly': Level_GoTo_Dynamics_TargetPairOnly,
                           'Level_GoTo_Dynamics_Test': Level_GoTo_Dynamics_Test,
                           })


# Goto Dynamic Hard

class Level_GoTo_Dynamics_Hard_Train(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               held_out_cp_pairs=[('green', 0), ('green', 2),
                                                  ('grey', 3), ('grey', 4),
                                                  ('blue', 1), ('blue', 5)], with_instruction=with_instruction)
        Level_GoTo.__init__(self, room_size=11, num_rows=3, num_dists=11,
                            num_cols=3, doors_open=False, seed=seed)

class Level_GoTo_Dynamics_Hard_TargetPairOnly(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['trap', 'flipud'],
                                                   'grey': ['fliplr', 'slippery'],
                                                   'blue': ['sticky', 'magic']}, with_instruction=with_instruction)
        Level_GoTo.__init__(self, room_size=11, num_rows=3, num_dists=11,
                            num_cols=3, doors_open=False, seed=seed)

class Level_GoTo_Dynamics_Hard_Test(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               with_instruction=with_instruction)
        Level_GoTo.__init__(self, room_size=11, num_rows=3, num_dists=11,
                            num_cols=3, doors_open=False, seed=seed)

class Level_GoTo_Dynamics_Hard_Fixed(DynamicsLevel, Level_GoTo):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['slippery', ],
                                                   'grey': ['flipud'],
                                                   'blue': ['fliplr'],
                                                   'red': ['trap'],
                                                   'purple': ['magic'],
                                                   'yellow': ['sticky'],
                                                   },
                               with_instruction=with_instruction)
        Level_GoTo.__init__(self, room_size=11, num_rows=3, num_dists=11,
                            num_cols=3, doors_open=False, seed=seed)

register_levels(__name__, {'Level_GoTo_Dynamics_Hard_Train': Level_GoTo_Dynamics_Hard_Train,
                           'Level_GoTo_Dynamics_Hard_TargetPairOnly': Level_GoTo_Dynamics_Hard_TargetPairOnly,
                           'Level_GoTo_Dynamics_Hard_Test': Level_GoTo_Dynamics_Hard_Test,
                           'Level_GoTo_Dynamics_Hard_Fixed': Level_GoTo_Dynamics_Hard_Fixed
                           })

# Unlock Dynamic
class Level_Unlock_Dynamic_Train(DynamicsLevel, Level_Unlock):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               held_out_cp_pairs=[('green', 0), ('green', 2),
                                                  ('grey', 3), ('grey', 4),
                                                  ('blue', 1), ('blue', 5)], with_instruction=with_instruction)
        Level_Unlock.__init__(self, room_size=11, num_rows=3, num_cols=3, seed=seed)

class Level_Unlock_Dynamic_TargetPairOnly(DynamicsLevel, Level_Unlock):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['trap', 'flipud'],
                                                   'grey': ['fliplr', 'slippery'],
                                                   'blue': ['sticky', 'magic']}, with_instruction=with_instruction)
        Level_Unlock.__init__(self, room_size=11, num_rows=3, num_cols=3, seed=seed)

class Level_Unlock_Dynamic_Test(DynamicsLevel, Level_Unlock):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               with_instruction=with_instruction)
        Level_Unlock.__init__(self, room_size=11, num_rows=3, num_cols=3, seed=seed)

class Level_Unlock_Dynamic_Fixed(DynamicsLevel, Level_Unlock):
    def __init__(self,
                 seed=None,
                 with_instruction=True
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['slippery', ],
                                                   'grey': ['flipud'],
                                                   'blue': ['fliplr'],
                                                   'red': ['trap'],
                                                   'purple': ['magic'],
                                                   'yellow': ['sticky'],
                                                   },
                               with_instruction=with_instruction)
        Level_Unlock.__init__(self, room_size=11, num_rows=3, num_cols=3, seed=seed)

register_levels(__name__, {'Level_Unlock_Dynamic_Train': Level_Unlock_Dynamic_Train,
                           'Level_Unlock_Dynamic_TargetPairOnly': Level_Unlock_Dynamic_TargetPairOnly,
                           'Level_Unlock_Dynamic_Test': Level_Unlock_Dynamic_Test,
                           'Level_Unlock_Dynamic_Fixed': Level_Unlock_Dynamic_Fixed
                           })


# Pickup Location Dynamic

class Level_PickupLoc_Dynamic_Train(DynamicsLevel, Level_PickupLoc):
    def __init__(self,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('blue', 4)])
        Level_PickupLoc.__init__(self, seed=seed)


class Level_PickupLoc_Dynamic_TargetPairOnly(DynamicsLevel, Level_PickupLoc):
    def __init__(self,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               color_property_map={'green': ['trap', ],
                                                   'blue': ['slippery', ]})
        Level_PickupLoc.__init__(self, seed=seed)


class Level_PickupLoc_Dynamic_Test(DynamicsLevel, Level_PickupLoc):
    def __init__(self,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2)
        Level_PickupLoc.__init__(self, seed=seed)

class Level_PickupLoc_Dynamic_Fixed(DynamicsLevel, Level_PickupLoc):
    def __init__(self,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 3, 4], n_floor_colors=2,
                               color_property_map={'green': ['slippery', ],
                                                   'red': ['trap'],
                                                   'yellow': ['sticky'],
                                                   },
                               )
        Level_PickupLoc.__init__(self, seed=seed)

register_levels(__name__, {'Level_PickupLoc_Dynamic_Train': Level_PickupLoc_Dynamic_Train,
                           'Level_PickupLoc_Dynamic_TargetPairOnly': Level_PickupLoc_Dynamic_TargetPairOnly,
                           'Level_PickupLoc_Dynamic_Test': Level_PickupLoc_Dynamic_Test,
                           'Level_PickupLoc_Dynamic_Fixed': Level_PickupLoc_Dynamic_Fixed
                           })


# Goto Sequential Dynamic

class Level_GotoSeq_Dynamic_Train(DynamicsLevel, Level_GoToSeq):
    def __init__(self,
                 seed=None
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               held_out_cp_pairs=[('green', 0), ('green', 2),
                                                  ('grey', 3), ('grey', 4),
                                                  ('blue', 1), ('blue', 5)])
        Level_GoToSeq.__init__(self, room_size=11, num_rows=3, num_cols=3, seed=seed)

class Level_GotoSeq_Dynamic_TargetPairOnly(DynamicsLevel, Level_GoToSeq):
    def __init__(self,
                 seed=None,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['trap', 'flipud'],
                                                   'grey': ['fliplr', 'slippery'],
                                                   'blue': ['sticky', 'magic']})
        Level_GoToSeq.__init__(self, room_size=11, num_rows=3, num_cols=3, seed=seed)

class Level_GotoSeq_Dynamic_Test(DynamicsLevel, Level_GoToSeq):
    def __init__(self,
                 seed=None,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3)
        Level_GoToSeq.__init__(self, room_size=11, num_rows=3, num_cols=3, seed=seed)

class Level_GotoSeq_Dynamic_Fixed(DynamicsLevel, Level_GoToSeq):
    def __init__(self,
                 seed=None,
                 ):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=3,
                               color_property_map={'green': ['slippery', ],
                                                   'grey': ['flipud'],
                                                   'blue': ['fliplr'],
                                                   'red': ['trap'],
                                                   'purple': ['magic'],
                                                   'yellow': ['sticky'],
                                                   }
                               )
        Level_GoToSeq.__init__(self, room_size=11, num_rows=3, num_cols=3, seed=seed)

register_levels(__name__, {'Level_GotoSeq_Dynamic_Train': Level_GotoSeq_Dynamic_Train,
                           'Level_GotoSeq_Dynamic_TargetPairOnly': Level_GotoSeq_Dynamic_TargetPairOnly,
                           'Level_GotoSeq_Dynamic_Test': Level_GotoSeq_Dynamic_Test,
                           'Level_GotoSeq_Dynamic_Fixed':Level_GotoSeq_Dynamic_Fixed
                           })

