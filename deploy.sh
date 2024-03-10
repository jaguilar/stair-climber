#! /bin/bash

SSH_TARGET="robot@ev3dev.local"
PROJECT_DIR=/home/robot/stair_climber
ssh "$SSH_TARGET" "mkdir -p $PROJECT_DIR"
scp *.py "$SSH_TARGET:$PROJECT_DIR"
ssh robot@ev3dev.local