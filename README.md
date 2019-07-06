# CryptoEye. Deploy on server Ubuntu 18

## INSTALL PYTHON & PIP

`sudo add-apt-repository ppa:jonathonf/python-3.6`  

> if it gives  ***add-apt-repository: command not found***   than use: `sudo apt-get install software-properties-common`

**Put each command separatly, one by one**
```
sudo apt update
sudo apt install python3.6
sudo apt install python3.6-dev
sudo apt install python3.6-venv
sudo apt-get install python3-distutils
sudo apt-get install build-essential
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.6 get-pip.py
sudo ln -s /usr/bin/python3.6 /usr/local/bin/python3
sudo ln -s /usr/local/bin/pip /usr/local/bin/pip3
sudo ln -s /usr/bin/python3.6 /usr/local/bin/python
```



## Install CryptoEye and Redis

```
sudo apt-get install git-core
git clone https://github.com/volkovartem77/cryptoeye.git
sudo apt install redis-server
sudo chown redis:redis /var/lib/redis
```


## Creating virtualenv using Python 3.6

```
sudo pip install virtualenv
virtualenv -p /usr/bin/python3.6 ~/cryptoeye/venv
cd ~/cryptoeye; . venv/bin/activate
pip install -r requirements.txt
python configure.py
deactivate
```


## Install & config supervisor


```
sudo apt-get install supervisor
sudo cp cryptoeye.conf /etc/supervisor/conf.d/cryptoeye.conf
sudo mkdir /var/log/cryptoeye
sudo mkdir /var/log/cryptoeye/websockets
sudo supervisorctl reread
sudo supervisorctl reload
```



## Start APP

You can put all these commands at once

```
sudo supervisorctl start all
sudo echo LAUNCHED
sudo supervisorctl status

```


## Usefull commands

```
sudo supervisorctl tail -5000 wsBinance stderr
sudo supervisorctl status
cd ~/cryptoeye; . venv/bin/activate
sudo nano /var/log/cryptoeye/wsBinance_ERR.log
```




