# Python base image
FROM python:3.9.19-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN MKDIR /app/abc

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 5001

# Command to run the application
CMD ["flask", "run"]
