ARG PYTHON_VERSION=${PYTHON_VERSION:-"3"}

FROM python:${PYTHON_VERSION}-alpine AS builder
MAINTAINER Michalski Luc <michalski.luc@gmail.com>

# change to app dir
WORKDIR /app

# install git and build-base (GCC, etc.)
RUN apk update && \
	  apk upgrade && \
    apk add --no-cache bash git openssh && \
    apk add build-base

# Update Pip3 
RUN python3 -m pip install --upgrade pip

# Install Pipenv
RUN pip3 install pipenv

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
	VIRTUAL_ENV="/opt/venv"

# install requirements first to engage docker cache
RUN python3 -m pip install -U pip && \
	  pip3 install flasgger

COPY requirements.txt .

RUN pip3 install -r requirements.txt

FROM python:${PYTHON_VERSION}-alpine AS runtime
MAINTAINER Luc Michalski <michalski.luc@gmail.com>

ARG VERSION
ARG BUILD
ARG NOW
ARG TINI_VERSION=${TINI_VERSION:-"v0.19.0"}

# Install tini to /usr/local/sbin
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-muslc-amd64 /usr/local/sbin/tini

# Install runtime dependencies & create runtime user
RUN apk --no-cache --no-progress add ca-certificates openssl libffi openblas libstdc++ \
 	&& chmod +x /usr/local/sbin/tini && mkdir -p /opt \
 	&& adduser -D bes -h /opt/bert-summary -s /bin/sh

# Switch to user context
USER bes
WORKDIR /opt/bert-summary

# Copy the virtual environment from the previous image
COPY --from=build /opt/venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH" \
	  VIRTUAL_ENV="/opt/venv"

# Set container labels
LABEL name="seoz-contrib-bert-summary" \
      version="$VERSION" \
      build="$BUILD" \
      architecture="x86_64" \
      build_date="$NOW" \
      vendor="seoz" \
      maintainer="Luc Michalski <michalski.luc@gmail.com>" \
      url="https://github.com/seoz.io/seoz-docker" \
      summary="SeoZ contrib - YAKE" \
      description="SeoZ contrib - YAKE" \
      vcs-type="git" \
      vcs-url="https://github.com/seoz.io/seoz-docker" \
      vcs-ref="$VERSION" \
      distribution-scope="public"

# Copy server startup script
COPY ./api.py /opt/bert-summary

ENV BERT_SUMMARY_PORT=${BERT_SUMMARY_PORT:-"5006"} \
	BERT_SUMMARY_HOST=${BERT_SUMMARY_HOST:-"0.0.0.0"}

# Container configuration
# Expose server port
EXPOSE "$BERT_SUMMARY_PORT"

# Set default command
ENTRYPOINT ["tini", "-g", "--"]
CMD [ "python", "api.py" ]
