FROM debian:latest

RUN apt-get update
RUN apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
RUN apt install python3 -y
RUN mkdir ~/server
WORKDIR /server

COPY server.py server.py
COPY index.html index.html

EXPOSE 8000

CMD ["python3", "server.py"]