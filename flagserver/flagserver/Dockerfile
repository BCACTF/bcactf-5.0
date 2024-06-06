FROM openjdk:22-jdk

WORKDIR /app

COPY . /app/flagserver

RUN javac flagserver/ChatServer.java

EXPOSE 54323

CMD ["java", "flagserver.ChatServer"]