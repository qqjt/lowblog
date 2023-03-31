---
title: Linux Desktop After Install Steps
date: 2022-12-12
updated: 2022-12-12
---
## 
```shell
sudo apt update
sudo apt install -y git vim openssh-server curl wget

```

## Oh My Zsh
<https://ohmyz.sh/>

```shell
sudo apt install zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
sudo reboot now # optional
```

## nodejs
```shell
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
# export PATH=~/.npm-global/bin:$PATH
```

## nvm

```shell
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
nvm install --lts
```

## Docker

<https://docs.docker.com/engine/install/ubuntu/>

```shell
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo groupadd docker
sudo usermod -aG docker $USER
```



## Software

- Google Chrome: <https://www.google.com/chrome/>
- DBeaver: <https://dbeaver.io/>
- Tabby: <https://tabby.sh/>
- Visual Studio Code: <https://code.visualstudio.com/>
- FreeFileSync: <https://freefilesync.org/download.php>
- WPS Office: <https://www.wps.com/office/linux/>
- JetBrains Toolbox: <https://www.jetbrains.com/toolbox-app/>
- nodejs: <https://github.com/nodesource/distributions/blob/master/README.md>