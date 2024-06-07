FROM node:20-bookworm

RUN useradd -m -d /home/ctf ctf

WORKDIR /home/ctf/app

RUN chown -R ctf:ctf /home/ctf/app

USER ctf

RUN bash -c "curl -fsSL https://deno.land/x/install/install.sh | sh"

COPY --chown=ctf:ctf ./server .

RUN npm ci

ENV PATH "${PATH}:/home/ctf/.deno/bin"
ENV NODE_ENV production

EXPOSE 3000

ENTRYPOINT ["npm", "start"]
