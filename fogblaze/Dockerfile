FROM node:20-bookworm

RUN apt-get update && apt-get install -y fonts-roboto

WORKDIR /ctf/app

COPY ./app .
COPY ./flag.txt ..

RUN npm ci
RUN npm run build

ENV HOST 0.0.0.0
ENV PORT 3000

EXPOSE 3000

ENTRYPOINT ["node", "build"]
