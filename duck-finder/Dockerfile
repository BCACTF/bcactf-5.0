FROM node:20-bookworm

RUN useradd -m -d /home/ctf ctf

USER ctf

RUN bash -c "curl -fsSL https://deno.land/x/install/install.sh | sh"

WORKDIR /home/ctf/app

COPY --chown=ctf:ctf ./entrypoint ./entrypoint
COPY --chown=ctf:ctf ./server ./server
COPY --chown=ctf:ctf ./flag.txt .

WORKDIR /home/ctf/app/entrypoint

RUN npm ci

ENV PATH "${PATH}:/home/ctf/.deno/bin"
ENV NODE_ENV production

EXPOSE 3000

ENTRYPOINT ["npm", "start"]
