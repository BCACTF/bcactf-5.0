FROM ubuntu:latest
RUN apt-get update && apt-get full-upgrade -y && apt-get install openjdk-17-jdk

COPY * .
RUN ./gradlew buildEnvironment && ./gradlew build