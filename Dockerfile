# Base image
FROM python:3.9-slim-buster AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY ./Pipfile ./Pipfile.lock /app/

# Install dependencies
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# Copy the project code to the container
COPY ./src /app/src

# Expose the port that the app will run on
EXPOSE 80

# Start the server
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
