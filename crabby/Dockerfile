FROM rust:1-slim-buster AS builder

WORKDIR /app

RUN apt-get update \
    && apt-get install -y pkg-config libssl-dev \
    && rm -rf /var/lib/apt/lists/* 

COPY rust/Cargo.toml . 

WORKDIR /app/src 

COPY rust/src .

WORKDIR /app

RUN cargo build --release


FROM python:3.12-slim-bookworm AS server

WORKDIR /app

COPY --from=builder /app/target/release/crabby /app/crabby

WORKDIR /app/server

COPY server/main.py .
COPY flag.txt ..

RUN pip install flask

EXPOSE 7787

ENTRYPOINT [ "python3", "main.py"]
