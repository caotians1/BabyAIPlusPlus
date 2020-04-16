# BabyAI++ : Towards Grounded-Language Learning beyond Memorization
This is the implementation of our paper "[BabyAI++ : Towards Grounded-Language Learning beyond Memorization](https://arxiv.org/pdf/2004.07200.pdf)", accepted 
to the ICLR2020 [BeTR-RL workshop](http://www.betr-rl.ml/2020/).


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
 
