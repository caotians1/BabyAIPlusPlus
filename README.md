# BabyAI++
This is the implementation of [BabyAI++ : Towards Grounded-Language Learning beyond Memorization](https://arxiv.org/pdf/2004.07200.pdf), as described in the following ICLR2020 [BeTR-RL](http://www.betr-rl.ml/2020/) workshop paper. 

```
@inproceedings{cao2020babiai++,
  title={BabyAI++ : Towards Grounded-Language Learning beyond Memorization},
  author={Cao, Tianshi and Wang, Jingkang and Zhang, Yining and Manivasagam, Sivabalan},
  booktitle={ICLR},
  year={2020}
}
```

## Introduction
Although recent works have shown the benefits of instructive texts in goal-conditioned RL, few have studied whether descriptive texts help agents to generalize across dynamic environments. To promote research in this direction, we introduce a new platform BabyAI++, to generate various dynamic environments along with corresponding descriptive texts (see following Table). Experiments on BabyAI++ show strong evidence that using descriptive texts improves the generalization of RL agents across environments with varied dynamics.

| <img width=290/>Environments                   | Instructive Text   | Descriptive Text   | State Manipulation | Variable Dynamics  | Procedural Envs    | Multi-task         |
|----------------------------------|:------------------:|:------------------:|:------------------:|:------------------:|:------------------:|:------------------:|
| [Kolve et al. (2017)](https://arxiv.org/abs/1712.05474)              | :x:                | :x:                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                |
| [Narasimhan et al. (2017)](https://arxiv.org/abs/1708.00133)         | :heavy_check_mark: | :x:                | :x:                | :x:                | :heavy_check_mark: | :x:                |
| [Wu et al. (2018)](https://arxiv.org/abs/1801.02209)                 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                | :x:                |
| [Chaplot et al. (2018)](https://arxiv.org/abs/1706.07230)            | :heavy_check_mark: | :x:                | :x:                | :x:                | :heavy_check_mark: | :x:                |
| [Chevalier-Boisvert et al. (2019)](https://arxiv.org/abs/1810.08272) | :heavy_check_mark: | :x:                | :heavy_check_mark: | :x:                | :heavy_check_mark: | :heavy_check_mark: |
| __BabyAI++ (Ours, 2020)__        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |


## Getting started
First, clone this repository to your local device recursively:
```bash
git clone --recursive https://github.com/caotians1/BabyAIPlusPlus.git
```
Install the prerequisites (Anaconda):
```bash
conda install pytorch=1.2.0 torchvision -c pytorch
conda install pyqt
pip install lorem tensorboardX blosc gym
```
Install `gym-minigrid` and `babyai`:
```bash
cd gym-minigrid
pip install --editable .
cd ../babyai
pip install --no-deps --editable .
```

## Using BabyAI++
Play a level in BabyAI++:
```
python experiment/gui.py --env="BabyAI-Level_GoToObj_Dynamics_Train-v0"
```
To train a model in BabyAI++, see `scripts/train_film_agent_redball.sh` and `experiment/train_rl.py`. 

## BabyAI++ Levels
Please refer to [`babyaiPP/dynamics_levels.py`](https://github.com/caotians1/BabyAIPlusPlus/blob/master/babyaiPP/dynamics_levels.py) and [`babyaiPP/additional_levels.py`](https://github.com/caotians1/BabyAIPlusPlus/blob/master/babyaiPP/additional_levels.py) for the definition of supported levels. The following table lists the available environments of BabyAI++ currently.

![babyai_levels](https://github.com/caotians1/BabyAIPlusPlus/blob/master/babyai_levels.png )


## Customize BabyAI++ Levels
You could also define your own environments with descriptive texts and varying dynamics. Here is an example for creating `PutNextLocalDynamics_Medium` Level:
```
# define dynamics setting
class Level_PutNextDynamics_Medium_Train(DynamicsLevel, Level_PutNext):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=2,
                               held_out_cp_pairs=[('green', 0), ('green', 2), ('green', 4),
                                                  ('blue', 1), ('blue', 3), ('blue', 5)],
                               with_instruction=with_instruction)
        Level_PutNext.__init__(self, room_size=11, seed=seed)

class Level_PutNextDynamics_Medium_Test(DynamicsLevel, Level_PutNext):
    def __init__(self, seed=None, with_instruction=True):
        DynamicsLevel.__init__(self, enabled_properties=[0, 1, 2, 3, 4, 5], n_floor_colors=2,
                               with_instruction=with_instruction)
        Level_PutNext.__init__(self, room_size=11, seed=seed)
        
# register your environment
register_levels(__name__, {'Level_PutNextDynamics_Medium_Train': Level_PutNextDynamics_Medium_Train})
```
Note that you could augument any levels supported in [BabyAI platform](https://github.com/mila-iqia/babyai) with varying dynamics and descriptive texts by inheriting `DynamicsLevel`.

## Questions/Bugs
Please submit a Github issue or contact jcao@cs.toronto.edu or wangjk@cs.toronto.edu if you have any questions or find any bugs. Contributions to this repository (e.g., pull requests for other baselines) are also well welcomed.
