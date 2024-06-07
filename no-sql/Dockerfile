FROM node:22-alpine

WORKDIR /app/server

COPY server/ .

ENV NODE_ENV production
RUN npm ci

EXPOSE 3000

CMD ["node", "app.js"]
