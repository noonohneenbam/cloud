# Use Python 3.8 base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY ./techtrends/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY ./techtrends ./

# Initialize the database
RUN python init_db.py

# Expose the application port
EXPOSE 3111

# Start the application
CMD ["python", "app.py"]
