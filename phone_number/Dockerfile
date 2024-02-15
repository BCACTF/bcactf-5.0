FROM ubuntu:latest
RUN apt-get update && apt-get install nginx -y && rm -rf /var/lib/apt/lists/*
WORKDIR /var/www/html
COPY . .
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]