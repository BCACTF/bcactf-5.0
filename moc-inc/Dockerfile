FROM python:3.12-bookworm

WORKDIR /app/server

COPY ./server .
COPY ./flag.txt ..

RUN pip install -r requirements.txt

EXPOSE 3000

ENTRYPOINT ["python3", "serve.py"]
