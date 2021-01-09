FROM python:3.8-slim AS builder

WORKDIR /opt/app

# Install Python and external dependencies, including headers and GCC
RUN apt update
RUN apt install --no-install-recommends  -y curl git cmake build-essential libgoogle-glog-dev libgflags-dev libeigen3-dev libopencv-dev libboost-dev libboost-all-dev libboost-iostreams-dev libcurl4-openssl-dev protobuf-compiler libopenblas-dev libhdf5-dev libprotobuf-dev libleveldb-dev libsnappy-dev liblmdb-dev libutfcpp-dev wget unzip 
# Update Pip3 
RUN python3 -m pip install --upgrade pip

# Install Nodejs and yarn
RUN rm -rf /var/lib/apt/lists/*
RUN curl -sL https://deb.nodesource.com/setup_12.x > node_install.sh
RUN chmod +x ./node_install.sh
RUN ./node_install.sh
RUN curl -sS http://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb http://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils nodejs yarn groff rsync
RUN apt install -y chromium
# Install Lighthouse
RUN yarn global add lighthouse

# Install Pipenv
RUN pip3 install pipenv

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
	VIRTUAL_ENV="/opt/venv"

COPY requirements.txt .

# Install dependencies into the virtual environment with Pipenv
RUN python3 -m pip install --upgrade pip
RUN pip3 --no-cache-dir install -r requirements.txt 
RUN pip3 install celery

ARG VERSION
ARG BUILD
ARG NOW
ARG TINI_VERSION=${TINI_VERSION:-"v0.19.0"}


# Install runtime dependencies & create runtime user
RUN mkdir -p /opt \
    mkdir -p bin config data logs

# Switch to user context
WORKDIR /opt/app

# Copy sources
COPY . .

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH" \
    VIRTUAL_ENV="/opt/venv"

# Set container labels
LABEL name="osat-server" \
      version="$VERSION" \
      build="$BUILD" \
      architecture="x86_64" \
      build_date="$NOW" \
      vendor="osat" \
      vcs-type="git" \
      vcs-ref="$VERSION" \
      distribution-scope="public"

# Container configuration
EXPOSE 8000
VOLUME ["/opt/app/data"]
ENTRYPOINT ["./docker-entrypoint.sh"]
# CMD ["./docker-entrypoint.sh"]