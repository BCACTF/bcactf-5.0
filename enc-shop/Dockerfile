FROM --platform=linux/amd64 ubuntu:20.04 AS build

RUN apt-get update -y && apt-get install -y gcc wget unzip && rm -rf /var/lib/apt/lists/*

RUN wget -Oynetd.c https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c \
    && gcc -o ynetd ynetd.c \
    && rm -f /tmp/ynetd.zip

FROM --platform=linux/amd64 python:3.12-slim-bookworm

RUN useradd -m -d /home/ctf -u 12345 ctf
WORKDIR /home/ctf

COPY server.py ./
COPY requirements.txt ./
COPY flag.txt ./

COPY --from=build ynetd ynetd
RUN chmod +x ynetd

RUN chown -R root:root /home/ctf
RUN pip install -r requirements.txt

USER ctf
EXPOSE 3000
CMD ["./ynetd", "-p", "3000", "python3 server.py"]
