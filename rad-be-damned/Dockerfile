FROM ubuntu

RUN apt update
RUN apt install python3-pip -y
RUN pip3 install flask
RUN pip3 install python-dotenv

WORKDIR /app

COPY . .

EXPOSE 3000

CMD ["python3", "-m", "flask", "run", "-p", "3000", "-h", "0.0.0.0"]