FROM python:3-alpine AS builder
MAINTAINER Luc Michalski <michalski.luc@gmail.com>

WORKDIR /opt/app

# Install Python and external dependencies, including headers and GCC
RUN apk add --no-cache libffi libffi-dev musl-dev gcc g++ git ca-certificates postgresql-dev mariadb-connector-c-dev

# Update Pip3 
RUN python3 -m pip install --upgrade pip

# Install Pipenv
RUN pip3 install pipenv

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
	VIRTUAL_ENV="/opt/venv"

COPY requirements.txt .

# Install dependencies into the virtual environment with Pipenv
RUN pip3 install -r requirements.txt 
RUN pip3 install celery

FROM python:3-alpine
MAINTAINER Luc Michalski <michalski.luc@gmail.com>

ARG VERSION
ARG BUILD
ARG NOW
ARG TINI_VERSION=${TINI_VERSION:-"v0.19.0"}

# Install tini to /usr/local/sbin
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-muslc-amd64 /usr/local/sbin/tini

# Install runtime dependencies & create runtime user
RUN apk --no-cache --no-progress add ca-certificates openssl libffi openblas libstdc++ mariadb-connector-c postgresql-client \
    && chmod +x /usr/local/sbin/tini && mkdir -p /opt \
    && adduser -D seoz -h /opt/seoz -s /bin/sh \
    && su seoz -c 'cd /opt/seoz; mkdir -p bin config data logs'

# Switch to user context
USER seoz
WORKDIR /opt/seoz

# Copy the virtual environment from the previous image
COPY --from=builder /opt/venv /opt/venv

# Copy sources
COPY . .

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH" \
    VIRTUAL_ENV="/opt/venv"

# Set container labels
LABEL name="seoz-server" \
      version="$VERSION" \
      build="$BUILD" \
      architecture="x86_64" \
      build_date="$NOW" \
      vendor="seoz" \
      maintainer="Luc Michalski <michalski.luc@gmail.com>" \
      url="https://github.com/seoz.io/seoz-docker" \
      summary="SeoZ project with Docker" \
      description="SeoZ project with Docker" \
      vcs-type="git" \
      vcs-url="https://github.com/seoz.io/seoz-docker" \
      vcs-ref="$VERSION" \
      distribution-scope="public"

# Container configuration
EXPOSE 5000
VOLUME ["/opt/seoz/data"]
ENTRYPOINT ["tini", "-g", "--"]
CMD ["./docker-entrypoint.sh"]