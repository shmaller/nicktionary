#!/bin/bash

# Add 'nicktionary' command to terminal
cd ~
touch .bashrc
echo "alias nicktionary='bash ~/github/nicktionary/scripts/nicktionary.sh'" >> .bashrc
