FROM node:20-bookworm

WORKDIR /app/server

COPY ./server .

RUN npm ci

ENV NODE_ENV production

EXPOSE 3000

ENTRYPOINT ["node", "app.js"]
