FROM gcc:4.9 AS builder

WORKDIR /app

COPY source.c .

RUN gcc -o flagprinter source.c -std=c99 -lm