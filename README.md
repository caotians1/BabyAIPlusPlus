# BabyAI++ : Towards Grounded-Language Learning beyond Memorization
This is the implementation of our paper "BabyAI++ : Towards Grounded-Language Learning beyond Memorization", accepted 
to 'Beyond “Tabula Rasa” in Reinforcement Learning (BeTR-RL): Agents that remember, adapt, and generalize' workshop
at ICLR2020. TODO: add arxiv link

## Getting started
First, clone this repository to your local device recursively:
```bash
git clone --recursive https://github.com/caotians1/BabyAIPlusPlus.git
```
Install the prerequisites (Anaconda):
```bash
conda install pytorch=0.4.1 torchvision -c pytorch
conda install pyqt numpy blosc
pip install gym
```
Install `gym-minigrid` and `babyai`:
```bash
cd gym-minigrid
pip install --editable .
cd ../babyai
pip install --no_deps --editable .
```
##Using BabyAI++
Play a level in BabyAI++:
```
python babyai/scripts/gui --env="BabyAI-Level_GoToObj_Dynamics_Train-v0"
```
To train a model in BabyAI++, see `scripts/train_film_agent_redball.sh` and `experiment/train_rl.py`.
 