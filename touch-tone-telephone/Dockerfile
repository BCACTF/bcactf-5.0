FROM rust:1.77

# For local testing on M1:
# FROM --platform=linux/amd64 rust:1.77


COPY gen /gen
WORKDIR /gen

COPY flag.txt ./flag.txt

RUN cargo run
