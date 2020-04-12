import gym
from babyai.levels.verifier import *
from babyai.levels.levelgen import *
from babyai.levels.iclr19_levels import *
from gym_minigrid.minigrid import DIR_TO_VEC
import copy

class DescriptiveLevel(RoomGridLevel):
    def __init__(self, description_level, desc_sample_frac, *args, **kwargs):
        print("entered descriptive level init")
        self.description_level = description_level  # type of description, 0 = no description, 1 = aggregated description, 2 = list description
        self.description_frac = desc_sample_frac  # if description is used, how much to use; 1 = describe everything
        self.desc = None
        super(DescriptiveLevel, self).__init__(*args, **kwargs)
        assert description_level in [0,1,2]

    def gen_mission(self):
        super(DescriptiveLevel, self).gen_mission()
        if self.description_level == 0:
            self.desc = None
            return
        # search for objects
        cell_infos = []
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                cell = self.grid.get(i, j)
                if cell is None:
                    continue
                if cell.type == "wall":
                    continue
                cell_infos.append((cell, i, j))

        if self.description_frac < 1:
            N = int(self.description_frac * len(cell_infos))
            inds = np.arange(len(cell_infos))
            np.random.shuffle(inds)
            cell_infos_new = [cell_infos[i] for i in inds[:N]]
            cell_infos = cell_infos_new

        if self.description_level == 1:

            self.desc, _, _ = gen_aggregated_description(cell_infos, agent_pos=self.agent_pos, agent_dir=self.agent_dir, aggregation_order="012")

        elif self.description_level == 2:
            descs = []
            for cell, i, j in cell_infos:
                desc = gen_description(cell, pos=(i,j), agent_pos=self.agent_pos, agent_dir=self.agent_dir)
                descs.append(desc)

            self.desc = " ".join(descs)

        return

    def step(self, action):
        obs, reward, done, info = super().step(action)
        obs['mission'] = self.desc
        return obs, reward, done, info

    def reset(self, **kwargs):
        obs = super().reset(**kwargs)
        obs['mission'] = self.desc
        return obs

def gen_aggregated_description(cell_info, agent_pos, agent_dir, aggregation_order):
    """
    :param aggregation_order: "type:0", "color:1", "direction:2",
    aggregation_order = 012: "there are are 2 keys, 2 red, one in front of you to your right and one in front of you to your left. There are 4 balls, 1 blue and 3 green..."
    aggregation_order = 201: "there are 3 objects in front of you to your left, 2 keys, 1 red and 1 green, and a box, 1 blue. There are 1 object in front of you to your right..."
    """
    # first, add a pos attribute to cells
    cell_info = copy.deepcopy(cell_info)
    all_types = []
    all_colors = []
    all_poses = []
    for cell, i, j in cell_info:
        v = (i - agent_pos[0], j - agent_pos[1])
        d1 = DIR_TO_VEC[agent_dir]
        d2 = (-d1[1], d1[0])
        pos = ""
        if dot_product(v, d1) > 0:
            pos += "F"
        elif dot_product(v, d1) < 0:
            pos += "B"
        if dot_product(v, d2) < 0:
            pos += "L"
        elif dot_product(v, d2) > 0:
            pos += "R"
        cell.pos = pos
        if cell.type not in all_types:
            all_types.append(cell.type)
        if cell.color not in all_colors:
            all_colors.append(cell.color)
        if cell.pos not in all_poses:
            all_poses.append(cell.pos)

    dims = {'type':all_types, 'color':all_colors, 'pos':all_poses}
    index = {'0':'type', '1':'color', '2':'pos'}
    t0 = index[aggregation_order[0]]
    t1 = index[aggregation_order[1]]
    t2 = index[aggregation_order[2]]
    dim_0 = dims[t0]
    dim_1 = dims[t1]
    dim_2 = dims[t2]
    count_array = np.zeros((len(dim_0), len(dim_1), len(dim_2)))

    for cell, i, j in cell_info:
        d0 = dim_0.index(getattr(cell, t0))
        d1 = dim_1.index(getattr(cell, t1))
        d2 = dim_2.index(getattr(cell, t2))
        count_array[d0,d1,d2] += 1

    desc = ""
    direction_list = {"FL":"front left",
                      "FR": "front right",
                      "BL": "back left",
                      "BR": "back right",
                      "B": "back",
                      "F": "front",
                      "R": "right",
                      "L": "left",
                      }

    ONEONEFLAG = 0

    for i in range(count_array.shape[0]):
        print(i)
        n_ins = count_array.sum(axis=(1,2))[i]
        if n_ins == 0:
            continue

        desc += "There "
        if n_ins == 1:
            desc += "is a "
            ONEONEFLAG = 1
        else:
            desc += "are %d " % n_ins
            ONEONEFLAG = 0
        value = dim_0[i]

        if t0 == "pos":
            content = direction_list[value]
            if n_ins > 1:
                desc += "objects to your " + content + ", "
            else:
                desc += "object to your " + content + ", "

        elif t0 == "type":
            desc += value
            if n_ins > 1:
                desc += "s, "
            else:
                desc += ", "
        else:
            desc += value + " object"
            if n_ins > 1:
                desc += "s, "
            else:
                desc += ", "

        for j in range(count_array.shape[1]):
            n_ins = count_array.sum(axis=(2,))[i, j]
            if n_ins == 0:
                continue
            if np.sum(count_array.sum(axis=(2,))[i, j:]) == n_ins:
                desc += "and "
            if ONEONEFLAG:
                if n_ins > 1:
                    desc += "%d " % n_ins
            else:
                desc += "%d " % n_ins

            if n_ins == 1:
                ONEONEFLAG = 1
            else:
                ONEONEFLAG = 0

            value = dim_1[j]

            if t1 == "pos":
                content = direction_list[value]
                desc += "to your " + content + ", "
            elif t1 == "type":
                desc += value
                if n_ins > 1:
                    desc += "s, "
                else:
                    desc += ", "
            else:
                desc += value + ", "

            for k in range(count_array.shape[2]):
                n_ins = count_array[i, j, k]
                if n_ins == 0:
                    continue
                if ONEONEFLAG:
                    if n_ins > 1:
                        desc += "%d " % n_ins
                else:
                    desc += "%d " % n_ins
                ONEONEFLAG = 0

                value = dim_2[k]

                if t2 == "pos":
                    content = direction_list[value]
                    desc += "to your " + content

                elif t2 == "type":
                    desc += value
                    if n_ins > 1:
                        desc += "s"
                else:
                    desc += value

                desc += ", "
            desc = desc[:-2] + "; "
        desc = desc[:-2] + ". "
    desc = desc[:-1]


    return desc, count_array, dims

def gen_description(cell, pos, agent_pos, agent_dir):
    # Direction from the agent to the object
    v = (pos[0] - agent_pos[0], pos[1] - agent_pos[1])

    # (d1, d2) is an oriented orthonormal basis
    d1 = DIR_TO_VEC[agent_dir]
    d2 = (-d1[1], d1[0])

    # Check if object's position matches with location
    pos_matches = {
        "left": dot_product(v, d2) < 0,
        "right": dot_product(v, d2) > 0,
        "in front of": dot_product(v, d1) > 0,
        "behind": dot_product(v, d1) < 0
    }
    s = "There is a %s %s " % (cell.color, cell.type)
    if dot_product(v, d1) > 0:
        s += "in front of you"
    elif dot_product(v, d1) < 0:
        s += "behind you"
    else:
        s += ""
    if dot_product(v, d2) < 0:
        s += ", on your left"
    elif dot_product(v, d2) > 0:
        s += ", on your right"
    s += "."
    return s
