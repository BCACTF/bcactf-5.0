FROM gcc:4.9 AS build

WORKDIR /app 
COPY . .
RUN apt-get update && apt-get install -y wget && wget -O ynetd.c \
    https://raw.githubusercontent.com/johnsonjh/ynetd/e6fd08f8f5d0c6b8c18d645957e30ce012536ed4/ynetd.c \
    && gcc -o ynetd ynetd.c && chmod +x ynetd && gcc -o celery main.c && chmod +x celery

EXPOSE 8989

ENTRYPOINT [ "./ynetd", "-p", "8989", "./celery" ]