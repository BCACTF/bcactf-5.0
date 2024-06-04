FROM python:3.12-bookworm

RUN apt update
RUN apt install python3-pip -y
RUN pip3 install flask
RUN pip3 install python-dotenv

WORKDIR /app

COPY . .

EXPOSE 3000
CMD ["python3", "main.py"]