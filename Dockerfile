FROM maven:latest AS build

WORKDIR /app

COPY . /app

RUN mvn clean package -DskipTests

FROM openjdk:17-jdk-slim

COPY --from=build /app/target/*.jar /app/application.jar

EXPOSE 8080

RUN ls -lah /app/application.jar

ENTRYPOINT ["java", "-jar", "/app/application.jar"]