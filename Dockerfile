# Use Python 3.13 as the base image
FROM python:3.13-slim

# Set working directory
WORKDIR /orgsvc


# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev libpq-dev\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY ./requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY ./ ./

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]