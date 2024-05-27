FROM node:20.04

WORKDIR /app

COPY package.json .

RUN npm ci 

COPY server.js .
COPY flag.txt .

WORKDIR /app/static

COPY static/ .

WORKDIR /app

EXPOSE 3000

ENTRYPOINT [ "node", "server.js" ]