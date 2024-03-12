#! /bin/bash

if uname -a | grep "microsoft.*WSL2" >/dev/null; then
    echo aliasing ssh
    export SSH="ssh.exe" 
    export SCP="scp.exe"
else
    SSH="ssh" 
    SCP="scp"
fi

SSH_TARGET="robot@ev3dev.local"
PROJECT_DIR=/home/robot/stair_climber
$SSH "$SSH_TARGET" "mkdir -p $PROJECT_DIR"
$SCP *.py "$SSH_TARGET:$PROJECT_DIR"
( $SSH -t "$SSH_TARGET" "cd $PROJECT_DIR && ( rm -f *.csv 2>/dev/null || /bin/true ) && brickrun -r -- pybricks-micropython main.py" || /bin/true )
mkdir -p ./.logs
$SCP "$SSH_TARGET:$PROJECT_DIR/*.csv" ./.logs