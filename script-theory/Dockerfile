FROM rust:1.78-bullseye

WORKDIR /addon

COPY ./src/addon .

RUN cargo build --release && \
    mv ./target/release/libscript_theory_addon.so ./libscript_theory_addon.node
