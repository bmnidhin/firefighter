# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3.9.12-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV AWS_ACCESS_KEY_ID=123 
ENV AWS_SECRET_ACCESS_KEY = 123
ENV AWS_DEFAULT_REGION=us-west-2

COPY . .

CMD [ "python3", "-m" , "cctv", "run"]