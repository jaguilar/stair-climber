#! /bin/bash

if uname -a | grep "microsoft.*WSL2" >/dev/null; then
    echo aliasing ssh
    export SSH="ssh.exe" 
    export SCP="scp.exe"
else
    export SSH="ssh" 
    export SCP="scp"
fi

SSH_TARGET="robot@ev3dev.local"
PROJECT_DIR=/home/robot/stair_climber
$SSH "$SSH_TARGET" "mkdir -p $PROJECT_DIR"
$SCP *.py "$SSH_TARGET:$PROJECT_DIR"
$SSH -t "$SSH_TARGET" "cd $PROJECT_DIR && brickrun -r -- pybricks-micropython main.py"