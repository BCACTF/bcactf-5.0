FROM ubuntu:latest

WORKDIR /app

COPY chall.c .

RUN apt-get update && apt-get install -y wget gcc \
    && wget -O ynetd.c https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c \
    && gcc -o ynetd ynetd.c \
    && gcc -o chall chall.c -fno-stack-protector -Wno-deprecated-declarations -no-pie -z,relro \
    && rm ynetd.c \
    && chmod +x chall && chmod +x ynetd \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 6896

ENTRYPOINT ["./ynetd", "-p", "6896", "/app/chall"]

