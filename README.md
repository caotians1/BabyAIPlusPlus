# BabyAI++ : Towards Grounded-Language Learning beyond Memorization
This is the implementation of [BabyAI++ : Towards Grounded-Language Learning beyond Memorization](https://arxiv.org/pdf/2004.07200.pdf), as described in the following ICLR2020 [BeTR-RL](http://www.betr-rl.ml/2020/) workshop paper. 

```
@inproceedings{cao2020babiai++,
  title={BabyAI++ : Towards Grounded-Language Learning beyond Memorization},
  author={Cao, Tianshi and Wang, Jingkang and Zhang, Yining and Manivasagam, Sivabalan},
  booktitle={AAAI},
  year={2020}
}
```

## Introduction
Although recent works have shown the benefits of instructive texts in goal-conditioned RL, few have studied whether descriptive texts help agents to generalize across dynamic environments. To promote research in this direction, we introduce a new platform, BabyAI++, to generate various dynamic environments along with corresponding descriptive texts (see following Table).

| <img width=300/>Environments                   | Instructive Text   | Descriptive Text   | State Manipulation | Variable Dynamics  | Procedural Envs    | Multi-task         |
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
pip install --no_deps --editable .
```

## Using BabyAI++
Play a level in BabyAI++:
```
python experiment/gui.py --env="BabyAI-Level_GoToObj_Dynamics_Train-v0"
```
To train a model in BabyAI++, see `scripts/train_film_agent_redball.sh` and `experiment/train_rl.py`.
 
