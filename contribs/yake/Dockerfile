ARG PYTHON_VERSION=${PYTHON_VERSION:-"3.7.1"}

FROM python:${PYTHON_VERSION}-alpine
MAINTAINER Michalski Luc <michalski.luc@gmail.com>

ARG YAKE_VERSION=${YAKE_VERSION:-"master"}

# change to app dir
WORKDIR /app

# install git and build-base (GCC, etc.)
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh && \
    apk add build-base

RUN pip install flasgger

# install requirements first to engage docker cache
RUN wget https://raw.githubusercontent.com/LIAAD/yake/${YAKE_VERSION}/requirements.txt -O requirements.txt && \
	pip install -r requirements.txt

# install yake via pip
RUN pip install git+https://github.com/liaad/yake.git@${YAKE_VERSION}

# Copy server startup script
COPY ./yake-rest-api.py /app

# Expose server port
ENV SERVER_PORT 5000
EXPOSE "$SERVER_PORT"

# set default command
CMD [ "python", "yake-rest-api.py" ]
