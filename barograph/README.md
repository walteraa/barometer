# Barograph

# Overview

Docker Compose for the Dashboard and Endpoints needed.

## How to Run

The instructions bellow, mainly the Installation of Docker CE and Docker Compose are chained to the Ubuntu environment, for more information read:

	1. [Install Docker CE](https://docs.docker.com/install/#docker-ce)
	2. [Install Docker Compose](https://docs.docker.com/compose/install/)

### Install Docker (Ubuntu 16.04 x86-64)

```
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce
sudo docker run hello-world
```

### Install Docker Compose (Ubuntu 16.04 x86-64)

```
sudo curl -L https://github.com/docker/compose/releases/download/1.20.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

### Build Application

Build the image so you can use it locally

```
docker build -t barograph .
```

Edit the `docker-compose.yml` to point to `barograph:lates` instead of `walteraa/barograph:latest`

### Deploy Application

```
docker-compose pull
docker-compose up -d # -d is for daemon
```

### Stop application

```
docker-compose down
```

### Update application

After you edit the application run:

```
docker-compose down
docker build -t barograph .
docker-compose pull
docker-compose up -d
```