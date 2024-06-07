FROM node:20.14

WORKDIR /app

COPY . .

RUN npm ci 

EXPOSE 3000

ENTRYPOINT [ "node", "server.js" ]