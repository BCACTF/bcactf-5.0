FROM openjdk:22-jdk

WORKDIR /app

COPY . /app/flagserver

RUN javac flagserver/ChatServer.java

CMD ["java", "flagserver.ChatServer"]
EXPOSE 54323
