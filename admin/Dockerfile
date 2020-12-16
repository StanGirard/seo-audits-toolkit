ARG NODE_VERSION=${NODE_VERSION:-"14"}

FROM mhart/alpine-node:${NODE_VERSION}
MAINTAINER Michalski Luc <michalski.luc@gmail.com>

# Set build arguments
ARG VERSION
ARG BUILD
ARG NOW

# Set Tini 
# Refs. https://github.com/krallin/tini#why-tini
ARG TINI_VERSION=${TINI_VERSION:-"v0.19.0"}

# Import project's dependencies
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install

# Copy source files
COPY . .

# Container configuration
EXPOSE 3000

VOLUME ["/app/build"]
LABEL name="seoz-admin" \
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

ENTRYPOINT ["tini", "-g", "--"]
CMD ["./docker-entrypoint.sh"]
