

#  webscrping-epaper



## Prerequisites
- [Docker] - [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
- [Docker Compose:] - [https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)

## Getting started

1.  create .env file from .env.sample
 
2. Start the `webscrping` service (and any others) in the background: 

    ```bash
    docker-compose up -d
    ```
 ## dev
 ```
 python3 -m venv venv 
 source venv/bin/activate
 pip install -r requirements.txt
 python -.py
 ```


