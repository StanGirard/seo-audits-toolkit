ARG PYTHON_VERSION=${PYTHON_VERSION:-"3.7.1"}

FROM python:${PYTHON_VERSION}-alpine AS builder

ARG YAKE_VERSION=${YAKE_VERSION:-"master"}

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

RUN python3 -m pip install -U pip && \
	pip3 install flasgger

# install requirements first to engage docker cache
RUN wget https://raw.githubusercontent.com/LIAAD/yake/${YAKE_VERSION}/requirements.txt -O requirements.txt && \
    pip3 install -r requirements.txt

# install yake via pip
RUN pip3 install git+https://github.com/liaad/yake.git@${YAKE_VERSION}

FROM python:3-alpine AS runtime


ARG VERSION
ARG BUILD
ARG NOW
ARG TINI_VERSION=${TINI_VERSION:-"v0.19.0"}

# Install tini to /usr/local/sbin
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-muslc-amd64 /usr/local/sbin/tini

# Install runtime dependencies & create runtime user
RUN apk --no-cache --no-progress add ca-certificates openssl libffi openblas libstdc++ \
 	&& chmod +x /usr/local/sbin/tini && mkdir -p /opt \
 	&& adduser -D yake -h /opt/yake -s /bin/sh

# Switch to user context
USER yake
WORKDIR /opt/yake

# Copy the virtual environment from the previous image
COPY --from=builder /opt/venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH" \
	VIRTUAL_ENV="/opt/venv"

# Set container labels
LABEL name="osat-contrib-yake" \
      version="$VERSION" \
      build="$BUILD" \
      architecture="x86_64" \
      build_date="$NOW" \
      vendor="osat" \
      url="https://github.com/osat.io/osat-docker" \
      summary="SeoZ contrib - YAKE" \
      description="SeoZ contrib - YAKE" \
      vcs-type="git" \
      vcs-url="https://github.com/osat.io/osat-docker" \
      vcs-ref="$VERSION" \
      distribution-scope="public"

# Copy server startup script
COPY ./api.py /opt/yake

ENV YAKE_PORT=${YAKE_PORT:-"5000"} \
	YAKE_HOST=${YAKE_HOST:-"0.0.0.0"}

# Container configuration
# Expose server port
EXPOSE "$YAKE_PORT"

# Set default command
ENTRYPOINT ["tini", "-g", "--"]
CMD [ "python", "api.py" ]
