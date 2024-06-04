FROM python:3.12

WORKDIR /app

ADD . /app

RUN pip install flask

EXPOSE 4321

CMD ["python", "server.py"]