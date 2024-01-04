FROM node:20-bookworm

WORKDIR /app/server

COPY ./server .
COPY ./flag.txt ..

RUN npm ci

ENV NODE_ENV production

EXPOSE 3000

ENTRYPOINT ["npm", "start"]
