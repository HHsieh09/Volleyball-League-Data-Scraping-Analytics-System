#!/bin/bash
# git clone https://github.com/HHsieh09/Volleyball-League-Data-Scraping-Analytics-System.git
# cd Volleyball-League-Data-Scraping-Analytics-System

echo "安裝 pyenv 所需套件..."
sudo apt-get update
sudo apt-get install -y docker.io
sudo apt-get install curl git bzip2 -y
curl https://pyenv.run | bash
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# 加入 shell 初始化設定
echo 'export LC_ALL=C.UTF-8' >> ~/.bashrc
echo 'export LANG=C.UTF-8' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/shims:$PATH"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
exec $SHELL

# 安裝 Python（可改其他版本）
echo "安裝 Python 3.9.21"
pyenv install 3.9.21
pyenv global 3.9.21
pyenv local 3.9.21

# Install poetry
pip install poetry
poetry env use 3.9.21
poetry sync