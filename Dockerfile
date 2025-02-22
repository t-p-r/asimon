# Purely for testing purposes, if it runs without Python error than it is good to go
FROM python:3.13-slim

WORKDIR /app

# Install pre-requisites
RUN pip install tabulate

# copy files over
COPY . .

# construct sample setup
COPY ./example/config/* ./src
COPY ./example/workspace ./src/workspace

FROM gcc:14.2.0

# sample invocation
CMD ["python", "src/stress.py"]