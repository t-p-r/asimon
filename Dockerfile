# Purely for testing purposes, if it runs without Python error than it is good to go
FROM python:3.13

WORKDIR /app

# Install pre-requisites
RUN apt-get update
RUN apt-get install -y g++
RUN pip install tabulate

# copy files over
COPY ./example ./example
COPY ./src ./src
COPY ./.gitmodules ./.gitmodules
# this is gruesome but is fast enough for now
COPY ./.git ./.git

# construct sample setup
COPY ./example/config/* ./src
COPY ./example/workspace ./src/workspace

# get testlib and CPDSA going
RUN git submodule update --init

CMD ["python", "src/stress.py"]