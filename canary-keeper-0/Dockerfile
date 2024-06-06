FROM --platform=linux/amd64 ubuntu@sha256:86ac87f73641c920fb42cc9612d4fb57b5626b56ea2a19b894d0673fd5b4f2e9 AS build

RUN apt-get update -y && apt-get install -y gcc wget && rm -rf /var/lib/apt/lists/*

RUN wget -O ynetd.c \
        https://raw.githubusercontent.com/johnsonjh/ynetd/e6fd08f8f5d0c6b8c18d645957e30ce012536ed4/ynetd.c \
    && echo "ec7509dec7737da54f8b18e1b5ba935d657f9f016c36cfc9ac08f9952373226f  ynetd.c" | sha256sum -c \
    && gcc -o ynetd ynetd.c

COPY chall.c .
RUN gcc -o chall  -fno-stack-protector chall.c

COPY provided.c .
RUN gcc -o provided -fno-stack-protector provided.c

FROM --platform=linux/amd64 ubuntu@sha256:86ac87f73641c920fb42cc9612d4fb57b5626b56ea2a19b894d0673fd5b4f2e9

RUN useradd -m -d /home/ctf -u 12345 ctf
WORKDIR /home/ctf

COPY --from=build ynetd ynetd
RUN chmod +x ynetd

COPY --from=build chall chall
COPY --from=build provided provided

RUN chown -R root:root /home/ctf

USER ctf
EXPOSE 9999
CMD ./ynetd -p 9999 ./chall