FROM gcc:14-bookworm AS builder

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/* \
    && wget -O ynetd.c https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c \
    && gcc -o ynetd ynetd.c && rm ynetd.c && chmod +x ./ynetd

FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

COPY --from=builder /ynetd /app/ynetd

COPY flag.txt /app/flag.txt
COPY main.py /app/main.py

EXPOSE 9031

ENTRYPOINT [ "./ynetd", "-p", "9031", "python3 main.py" ]