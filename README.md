# Nicktionary

This is a Python clone of the game Wordle, written by Nicholas Boni, originally made by Josh Wardle.

The game updates the Wordle every day until October 20, 2027. After that point, it will pull a random word from the list of 2,315 possible solutions.

## Background

Josh Wardle's original game Wordle was sold to a newspaper which abandoned his original word list. This game uses the original list, and so is equivalent to playing the old Wordle game on his website. The point of making this was 1. for fun, and 2. to keep Wordle "hard and weird".

## Installation
### Prerequisites
- Git and Python 3.x must be installed.

### Download 

Clone this repository:

```bash
mkdir ~/github 2> /dev/null
cd ~/github
git clone https://github.com/shmaller/nicktionary.git
```

### Run

```bash
python3 ~/github/nicktionary/src/nicktionary.py
```

### Recommended one-time setup: Add `nicktionary` command to terminal

I recommend adding the `nicktionary` command to your terminal configuration, allowing you to run Nicktionary
from a single command. Copy and paste the appropriate command for your system into your terminal:

#### Mac (zsh terminal)

```bash
touch ~/.zshrc
cat >> ~/.zshrc <<'EOF'
nicktionary() {
  dir=$(pwd)
  echo "Checking for updates..."
  cd ~/github/nicktionary
  git pull || echo "Couldn't update; connection to GitHub failed."
  cd $dir
  python3 ~/github/nicktionary/src/nicktionary.py
}

EOF

source ~/.zshrc
```

#### Linux (bash terminal)

```bash
touch ~/.bashrc
cat >> ~/.bashrc <<'EOF'
nicktionary() {
  dir=$(pwd)
  echo "Checking for updates..."
  cd ~/github/nicktionary
  git pull || echo "Couldn't update; connection to GitHub failed."
  cd $dir
  python3 ~/github/nicktionary/src/nicktionary.py
}

EOF

source ~/.bashrc
```

Afterwards you can run Nicktionary simply:

```bash
nicktionary
```

## How to play

1. Enter `play` to play today's word.
2. Guess a five-letter word.
3. The game will tell you if the each letter of your guess appears in the solution word.

You have six guesses to get it right!

Use the interactive `help` to learn the rules and the interface!
