FROM node:20.14

WORKDIR /app

COPY . .

RUN npm ci 

RUN adduser ctf

USER ctf

EXPOSE 3000

ENTRYPOINT [ "node", "server.js" ]