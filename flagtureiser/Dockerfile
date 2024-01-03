FROM amazoncorretto:latest

COPY source/ .
RUN ./gradlew buildEnvironment && ./gradlew build
