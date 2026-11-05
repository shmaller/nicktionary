mkdir ~/github 2> /dev/null
cd ~/github
git clone https://github.com/shmaller/nicktionary.git

cd ~
touch .bashrc
echo "alias nicktionary='bash ~/github/nicktionary/scripts/nicktionary.sh'" >> .bashrc
