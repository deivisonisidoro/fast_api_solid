# Base image
FROM python:3.9-slim-buster AS base

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Start server
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
