# Airelogic
**Ops-Tech-Test**

## **_Objective 1: Echo Server_**

Create a **docker container** named **‘greeter’** which runs a http server. The server should
return “Hello, my name is $NAME”, where $NAME is an environment variable.

_Restrictions_

- You must use the official Debian docker image (https://hub.docker.com/_/debian) as
the base image for this container
-  The http server can be written in any language you want
- You must not use a pre-made image that provides this functionality; you must write it
yourself.

## Solution

In the folder **flask** you can find two files:

**server.py:**
- Web server _(http)_ developed with python framework **Flask** 
- Environment variable <NAME>, passed by the **os** python library connecting the docker container with the app
 
**dockerfile**:
 
- With **Debian** latest image as base, _install_ the necesary dependencies:

    | command |  packages |  explanation |
    | ------ | ------ | ------ |
    | apt-get update|  |updating the managing tool for packages |
    | apt install | wget build-essential | set of build-essential packages for Debian |
    | apt-get install  | python-pip  |  package installer for Python |
    | pip3 install | flask | web framework written in Python. |

- Create a copy of the web server code into the image from the local machine (repository).
- Run the python script to allow the server process to start.

    
## Dependencies
To run a test for the first objetive follow the next step:

1. Build a web server **docker image**: 
```sh
#docker image build <tag> <image_tag> <source>
docker image build -t web_py flask/
```
2. Run the image in **docker container** in _deteach mode_: 
```sh
#docker container run <detach_mode> <STDIN_open><pseudo-TTY> <name> <local_machine_port:container_port> <image_name>
docker container run -d --name greeter -it --name proxy_cont -p 8080:5000 web_py
```
3. Check the url
> Note: $NAME need to be the same as the variable set in docker image.
```sh
curl -i localhost:5000/${NAME}
```


## **_Objective 2: Reverse Proxy_**

Create a **docker container** named **‘reverse-proxy’** which runs a http reverse proxy of your
choice (e.g. nginx, apache).

The reverse proxy should have two targets, one named **Alice** and the other named **Bob**. They should be routed by path, so for example going to /alice routes you to Alice, and going to /bob routes you to Bob.

_Restrictions_

- You must use the official CentOS docker image (https://hub.docker.com/_/centos) as
the base image for this container
- You must not use a pre-made image that provides this functionality; you must write it
yourself.

## Solution

In the folder **reverse_prox** you can find two files:

**nginx.conf:**
- Nginx configuration file pointing to **/alice** and **/bob** path as a proxy server. 
- The way to add this file into the docker container is done by volume explained in the _dependcies_ steps
volume**
    
**dockerfile:**
- With **Centos** latest image, we _install_ the necesary dependencies

    | command |  packages |  explanation |
    | ------ | ------ | ------ |
    | yum install| epel-release  |set of extra packages for RHEL |
    | yum install | nginx |  HTTP and reverse proxy server |

- Expose the nginx-container port: _80_
- Run the command to start nginx server

## Dependencies
To run a test for the second objetive follow the next step:

1. Build the proxi server **docker image**: 
```sh
#docker image build <tag> <image_tag> <source>
docker image build -t proxy reverse_prox/
```
2. Run the image in **docker container** in _deteach mode_: 
```sh
#docker container run <detach_mode> <STDIN_open><pseudo-TTY> <name> <local_machine_port:container_port> <image_name>
docker container run -d --name nginx_proxy -it -p 8080:80 -v ./Airelogic/reverse_prox/nginx.conf:/etc/nginx/nginx.conf proxy
```
> Note: || -v (volume) ||  preferred mechanism for persisting data. In this case, the volume is mounted directly from our local machine (repository) to the nginx.conf file located in the nginx files configuration, allowing the file replacement.

3. Test the NGINX container 

```sh
curl -i localhost:8080/
```


## _**Objective 3: Put it all together**_

Create a docker-compose.yml such that, when you call docker-compose up:

- There are two instances of **greeter**, one called _alice_ and the other _bob_.
    - **Alice** should answer with _“Hello, my name is Alice”_
    - **Bob** should answer with _“Hello, my name is Bob”_
- There is a **reverse-proxy** which points to alice and bob
- Only the reverse-proxy should be exposed to the local network, on port **8080**
- The two greeter instances should **not be accessible** except via **reverse-proxy**!

In the main folder of the reposiroty there is a docker-compose file:

**docker-compose.yaml:**

- Set the version: **3.7**
- Declare two type of services:
    -  2 web_app instances: alice and bob
    
        | service_name | **alice** or **bob** |
        | ------ | ------ |
        | image | web_py |
        | environment | **Alice** or **Bob** |
        | expose_port | 5000 |
        | networks| internal_network_1 |
    
    - 1 nginx_proxy instance: nginx_prox
    
        | service_name | **nginx_proxy** |
        | ------ | ------ |
        | image | prox |
        | service_name | **nginx_proxy** |
        | depends_on | alice,  bob |
        | volumes| ./Airelogic/reverse_prox/nginx.conf:/etc/nginx/nginx.conf |
        | port | 8080 |
        | networks| internal_network_1, extenal_network|
>Note: the volume path needs to be set depending on the host OS, following the linux or windows path normative.
- Declare and create networks

    | external_network||
    | ------ | ------ |
    | name | external_network |
    
    | internal_network||
    | ------ | ------ |
    | external | false |
    | name | internal_network |

## Dependencies
To run a **manual test** for the third objetive follow the next step:

Make sure the two images (web_py / prox ) are already built, if not check the build-image dependencies for objectives 1 & 2.

1. Run the docker-compose file:
```sh
docker-compose up -d
```
>Note: **-d** deteach mode

2. Test the container deployed
```sh
curl -i localhost:8080/ # Http 404
```
```sh
curl -i localhost:8080/alice # "Hello, my name is alice"
```
```sh
curl -i localhost:8080/bob # "Hello, my name is Bob"
```
```sh
curl -i localhost:8080/nico # Http 404
```
