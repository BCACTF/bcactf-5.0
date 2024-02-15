FROM ubuntu:latest as build

RUN apt-get update -y && apt-get install -y gcc && apt-get install -y wget && apt-get install -y unzip && rm -rf /var/lib/apt/lists/*

RUN wget -O ynetd.c https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c \
  && gcc -o ynetd ynetd.c \
  && rm -f /tmp/ynetd.zip


FROM --platform=linux/amd64 python:3.8-slim-buster AS deployer

RUN useradd -m -d /home/ctf -u 12345 ctf
WORKDIR /home/ctf

# copy over ynetd
COPY --from=build ynetd ynetd 
RUN chmod +x ynetd

# copy over source and set permissions
COPY physics-test.py physics-test.py 
RUN chown -R root:root /home/ctf


# run and expose
USER ctf
EXPOSE 9999
CMD ["./ynetd", "-p", "8148", "python3 physics-test.py"]