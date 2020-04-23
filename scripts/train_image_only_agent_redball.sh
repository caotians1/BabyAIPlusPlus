#!/usr/bin/env bash
frames=5000000
batch_size=12800
procs=256
log_interval=2
env=BabyAI-GoTo_RedBallDynamics_Train-v0

python experiment/train_rl.py --env $env --arch cnn --no-desc --tb --frames $frames --batch-size $batch_size --procs $procs --log-interval $log_interval
