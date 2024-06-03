FROM --platform=linux/amd64 python:3.12-slim-bookworm AS build

RUN apt-get update -y \
    && apt-get install -y gcc wget \
    && rm -rf /var/lib/apt/lists/* \
    && wget -O ynetd.c https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c \
    && gcc -o ynetd ynetd.c


FROM --platform=linux/amd64 python:3.12-slim-bookworm AS deployer

RUN useradd -m -d /home/ctf -u 12345 ctf
WORKDIR /home/ctf

# copy over ynetd
COPY --from=build ynetd ynetd 
RUN chmod +x ynetd && chown -R ctf:ctf /home/ctf 

USER ctf

COPY ./flag.txt .
COPY ./rsa_encrypter.py .

RUN pip install pycryptodome==3.20.0

CMD ["./ynetd", "-p", "3000", "python3 ./rsa_encrypter.py"]