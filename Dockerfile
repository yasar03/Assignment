# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Define environment variable for SQLite database
ENV DATABASE_URI="sqlite:///game_data.db"

# Command to run the Flask application
CMD ["python", "./app.py"]
