# Airelogic
Nicolas M. Morillo Ops-Tech-Test


Objective 1: Echo Server --> flask folder

Content:
    Dockerfile 
    server.py

    server.py:
    - The web server has been develop using the framework Flask.  
    - The <def hello()> use the enviroment var to create the path for the url

    Dockerfile: 
    - Using the given Debian image, install the necesary dependencies to update apt-get, install python, python-pip and flask.
    - Create a copy of the web server code into the image from the local machine.
    - Run the python script to allow the server process start.
    
-- Test container:
docker image build -t flask2 flask/
docker container run -d -it -p 8080:5000 flask2

curl localhost:8080/NAME # Variable specified in the dockerfile 

Objective 2: Reverse Proxy --> reserve_prox folder

Content:
    Dockerfile
    nginx.conf

    Dockerfile:
    - With the given Centos image, install the epel-release to be able install future binary, and install nginx
    - Expose the nginx-container port
    - Run the command to start nginx server

    nginx.conf:
    - Nginx configuration file pointed to the Alicia and Bob url path as a proxy server. 
    - This configure file will be add and swap with the original, into the container using the volume as persisten storage location

-- Test container:
docker image build -t prox reverse_prox/
docker container run -d -it -p 8080:80 /
    -v /$PWD/reserve_prox/nginx.conf:/etc/nginx/nginx.conf


Objective 3: Put it all together --> docker-compose.yaml

Content:
    docker-compose.yaml:

    - Two web_server as instances with the names alice and bob, the environment variable set with alice and bob and networks
    - Nginx proxy container with the port expose and the networks created by the docker-compose
    - Creation of network necesaries to connect all container

-- Test compose:
docker image build -t flask2 flask/
docker image build -t prox reverse_prox/
docker-compose up -d

curl localhost:8080/alice
curl localhost:8080/bob
curl localhost:8080/nico
