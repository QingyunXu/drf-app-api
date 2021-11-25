#############################################
# Basic Env & packages                      #
#############################################

FROM python:3.8-alpine

# run python in unbuffered mode
ENV PYTHONUNBUFFERED 1

# copy requirement file to docker
COPY ./requirements.txt /requirements.txt
# add package on container
RUN apk add --update --no-cache postgresql-client jpeg-dev
# install temp dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# install packages in requirement file
RUN pip install -r /requirements.txt
# lease temp dependencies
RUN apk del .tmp-build-deps


#############################################
# Working directory                         #
#############################################

RUN mkdir /app
# default working directory
WORKDIR /app
# copy from local machine to docker
COPY ./app /app

# set a static file dir
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

#############################################
# Authentication                            #
#############################################

# create user in docker, username is qingyun
RUN adduser -D qingyun
# change permissions for dir
RUN chown -R qingyun:qingyun /vol/
RUN chmod -R 755 /vol/web
# switch to docker to the user qingyun
USER qingyun