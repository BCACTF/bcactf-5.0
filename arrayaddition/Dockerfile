FROM --platform=linux/amd64 ubuntu:latest

RUN apt-get update -y && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY main.c .
RUN gcc -o arrayaddition main.c
