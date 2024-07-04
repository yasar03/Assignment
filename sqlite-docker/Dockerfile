# Use an Alpine Linux base image with SQLite
FROM alpine:latest

# Install SQLite
RUN apk add --no-cache sqlite

# Set the working directory
WORKDIR /data

# Copy the database file into the container
COPY game_data.db /data/game_data.db

# Command to start SQLite
CMD ["sqlite3", "game_data.db"]

# sqlite-docker/Dockerfile



# FROM nouchka/sqlite3

# COPY ./game_data.db /data/game_data.db

# CMD ["sqlite3", "/data/game_data.db", ".databases"]

