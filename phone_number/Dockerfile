FROM python:3.12
WORKDIR /

RUN pip install flask

#idk if i need this but just in case
COPY . . 

EXPOSE 5000
CMD ["flask", "--app", "server","run"]

#i really hope this works