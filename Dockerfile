# Purely for testing purposes, if it runs without Python error than it is good to go
FROM gcc:14.2.0

WORKDIR /app

# RUN pip install pyinstaller
RUN apt-get update
# RUN apt-get install python -y
RUN apt-get install python3-tabulate -y

# copy files over
COPY . .

# construct sample setup
COPY ./example/config/* ./src
COPY ./example/workspace ./src/workspace

# sample invocation
RUN python3 ./src/stress.py
RUN python3 ./src/create_problem.py