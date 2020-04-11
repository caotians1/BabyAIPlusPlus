#!/usr/bin/env python3

"""
Evaluate a trained model or bot
"""

import argparse
import gym
import time
import datetime
import math
import babyai.utils as utils
from babyai.evaluate import evaluate_demo_agent, batch_evaluate, evaluate
# Parse arguments

parser = argparse.ArgumentParser()
parser.add_argument("--exp_name", required=True, type=str)
parser.add_argument("--env", required=True,
                    help="name of the environment to be run (REQUIRED)")
parser.add_argument("--model", default=None,
                    help="name of the trained model (REQUIRED or --demos-origin or --demos REQUIRED)")
parser.add_argument("--episodes", type=int, default=1000,
                    help="number of episodes of evaluation (default: 1000)")
parser.add_argument("--seed", type=int, default=int(1e9),
                    help="random seed")
parser.add_argument("--argmax", action="store_true", default=False,
                    help="action with highest probability is selected for model agent")

def main_train(args, seed, episodes):
    # Set seed for all randomness sources
    utils.seed(seed)

    # Define agent
    # do train environment
    env_name = args.env + "_Train-v0"
    env = gym.make(env_name)
    env.seed(seed)
    agent = utils.load_agent(env, args.model, argmax=args.argmax, env_name=env_name)
    if args.model is None and args.episodes > len(agent.demos):
        # Set the number of episodes to be the number of demos
        episodes = len(agent.demos)

    # Evaluate
    if isinstance(agent, utils.DemoAgent):
        logs = evaluate_demo_agent(agent, episodes)
    elif isinstance(agent, utils.BotAgent):
        logs = evaluate(agent, env, episodes, False)
    else:
        logs = batch_evaluate(agent, env_name, seed, episodes)

    return logs


def main_test(args, seed, episodes):
    # Set seed for all randomness sources
    utils.seed(seed)

    # Define agent
    # do test environment
    env_name = args.env + "_Test-v0"
    env = gym.make(env_name)
    env.seed(seed)
    agent = utils.load_agent(env, args.model, argmax = args.argmax, env_name=env_name)
    if args.model is None and args.episodes > len(agent.demos):
        # Set the number of episodes to be the number of demos
        episodes = len(agent.demos)

    # Evaluate
    if isinstance(agent, utils.DemoAgent):
        logs = evaluate_demo_agent(agent, episodes)
    elif isinstance(agent, utils.BotAgent):
        logs = evaluate(agent, env, episodes, False)
    else:
        logs = batch_evaluate(agent, env_name, seed, episodes)

    return logs

if __name__ == "__main__":
    args = parser.parse_args()

    start_time = time.time()
    logs = main_train(args, args.seed, args.episodes)
    logs_ts = main_test(args, args.seed, args.episodes)
    end_time = time.time()

    # Print logs
    return_per_episode_tr = utils.synthesize(logs["return_per_episode"])
    success_per_episode_tr = utils.synthesize(
        [1 if r > 0 else 0 for r in logs["return_per_episode"]])

    num_frames_per_episode_tr = utils.synthesize(logs["num_frames_per_episode"])
    succ_se_tr = math.sqrt(success_per_episode_tr['mean'] * (1 - success_per_episode_tr['mean']) / args.episodes)
    R_se_tr = return_per_episode_tr['std']/math.sqrt(args.episodes)
    N_se_tr = num_frames_per_episode_tr['std']/math.sqrt(args.episodes)

    return_per_episode_ts = utils.synthesize(logs_ts["return_per_episode"])
    success_per_episode_ts = utils.synthesize(
        [1 if r > 0 else 0 for r in logs_ts["return_per_episode"]])

    num_frames_per_episode_ts = utils.synthesize(logs_ts["num_frames_per_episode"])
    succ_se_ts = math.sqrt(success_per_episode_ts['mean'] * (1 - success_per_episode_ts['mean']) / args.episodes)
    R_se_ts = return_per_episode_ts['std'] / math.sqrt(args.episodes)
    N_se_ts = num_frames_per_episode_ts['std'] / math.sqrt(args.episodes)

    print(
        "{} & ${:.3f}\pm{:.3f}$ & ${:.3f}\pm{:.3f}$ & ${:.3f}\pm{:.3f}$ & ${:.3f}\pm{:.3f}$ & ${:.3f}\pm{:.3f}$ & ${:.3f}\pm{:.3f}$ \\\\"
        .format(args.exp_name, success_per_episode_tr['mean'], succ_se_tr, return_per_episode_tr['mean'], R_se_tr,
                num_frames_per_episode_tr['mean'], N_se_tr,
                success_per_episode_ts['mean'], succ_se_ts, return_per_episode_ts['mean'], R_se_ts,
                num_frames_per_episode_ts['mean'], N_se_ts))
