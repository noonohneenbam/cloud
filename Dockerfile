# Use Python 3.8 base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# LAbel
LABEL maintainer="Udacity is fun?"

# Copy application code and dependencies
COPY . /app
COPY ./techtrends ./
# Install system dependencies for SQLite and Python packages
RUN apt-get update && apt-get install -y sqlite3 && \
    pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt
# Initialize the database
RUN python init_db.py

# Expose the application port
EXPOSE 3111

# Set the command to run the application
CMD ["python", "app.py"]
