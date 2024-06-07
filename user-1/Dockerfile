FROM python:3.12-slim-bookworm

RUN useradd -ms /bin/bash bcactf && chown -R bcactf:bcactf /home/bcactf

USER bcactf

WORKDIR /home/bcactf

COPY --chown=bcactf:bcactf . .

RUN pip install flask && mkdir -p /home/bcactf/dbs

EXPOSE 7272

CMD [ "python", "server.py", "7272" ]