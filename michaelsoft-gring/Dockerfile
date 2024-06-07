FROM python:3.12-slim-bookworm

WORKDIR /app

RUN useradd -m bcactf && chown -R bcactf:bcactf /app && chmod -R 775 /app

ENV PATH $PATH:/home/bcactf/.local/bin
RUN pip install flask

COPY . . 

USER bcactf
EXPOSE 5000
ENTRYPOINT ["python", "server.py"]