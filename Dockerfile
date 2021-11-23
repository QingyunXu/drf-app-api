#############################################
# Basic Env & packages
#############################################

FROM python:3.8-alpine

# run python in unbuffered mode
ENV PYTHONUNBUFFERED 1

# copy requirement file to docker
COPY ./requirements.txt /requirements.txt
# add package on container
RUN apk add --update --no-cache postgresql-client
# install temp dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
# install packages in requirement file
RUN pip install -r /requirements.txt
# lease temp dependencies
RUN apk del .tmp-build-deps


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