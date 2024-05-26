FROM node:20.04

RUN apt-get update && apt-get install -y curl gcc wget && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && wget -O ynetd.c https://raw.githubusercontent.com/johnsonjh/ynetd/e6fd08f8f5d0c6b8c18d645957e30ce012536ed4/ynetd.c \
    && echo "ec7509dec7737da54f8b18e1b5ba935d657f9f016c36cfc9ac08f9952373226f  ynetd.c" | sha256sum -c \
    && gcc -o ynetd ynetd.c && chmod +x ./ynetd && mv ynetd /usr/local/bin/ynetd && rm ynetd.c \
    && export PATH=$PATH:/usr/local/bin

WORKDIR /app

COPY . /app/

EXPOSE 8898

ENTRYPOINT ["ynetd", "-p", "8898", "node", "main.js"]
