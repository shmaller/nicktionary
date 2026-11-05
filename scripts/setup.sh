#!/bin/bash

# Download source code from GitHub
mkdir ~/github 2> /dev/null
cd ~/github
git clone https://github.com/shmaller/nicktionary.git

# Add 'nicktionary' command to terminal
cd ~
touch .bashrc
echo "alias nicktionary='bash ~/github/nicktionary/scripts/nicktionary.sh'" >> .bashrc
