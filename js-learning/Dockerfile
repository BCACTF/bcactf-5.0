FROM node:20.14

RUN useradd -m ctf -d /app && chown -R ctf:ctf /app

USER ctf

WORKDIR /app

COPY . .

RUN npm ci && chmod 550 /app

RUN adduser ctf

USER ctf

EXPOSE 3000

ENTRYPOINT [ "node", "server.js" ]