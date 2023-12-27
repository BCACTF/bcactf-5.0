FROM amazoncorretto:latest

COPY src/* .
RUN ./gradlew buildEnvironment && ./gradlew build