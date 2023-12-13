FROM python:3.12-bookworm

WORKDIR /app/server

COPY ./server .

RUN pip install -r requirements.txt

WORKDIR /app

COPY ./ynetd .
COPY ./flag.txt .

RUN chmod +x ./ynetd

ENTRYPOINT ["./ynetd", "-p", "3000", "python3 ./server/server.py"]
