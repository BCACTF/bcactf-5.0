FROM ubuntu:latest as builder 
RUN apt-get upgrade -y && apt-get update -y && apt-get install -y gcc wget && rm -rf /var/lib/apt/lists/* 
WORKDIR /app
COPY xor.c .
RUN gcc -o xor xor.c
RUN wget https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c && gcc -o ynetd ynetd.c


FROM ubuntu:latest as runner
WORKDIR /app
COPY --from=builder /app/xor .
COPY --from=builder /app/ynetd .
COPY flag.txt .
RUN chmod +x xor ynetd
CMD ["./ynetd", "-p", "3012", "./xor"]