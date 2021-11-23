#############################################
# Basic Env & packages
#############################################

FROM python:3.8-alpine

# run python in unbuffered mode
ENV PYTHONUNBUFFERED 1

# copy requirement file to docker
COPY ./requirements.txt /requirements.txt

# install packages in requirement file
RUN pip install -r /requirements.txt


#############################################
# Working directory
#############################################

RUN mkdir /app
# default working directory
WORKDIR /app
# copy from local machine to docker
COPY ./app /app


#############################################
# Authentication
#############################################

# create user in docker, username is qingyun
RUN adduser -D qingyun
# switch to docker to the user qingyun
USER qingyun