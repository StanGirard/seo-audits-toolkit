ARG NODE_VERSION=${NODE_VERSION:-"14"}

FROM mhart/alpine-node:${NODE_VERSION} AS front-builder
MAINTAINER Michalski Luc <michalski.luc@gmail.com>

# Import project's dependencies
WORKDIR /app

COPY package.json ./

RUN yarn install --network-timeout 1000000000

# Copy source files
COPY . .

RUN yarn build

FROM caddy:2.3.0-rc.1-builder-alpine AS caddy-builder 
MAINTAINER Michalski Luc <michalski.luc@gmail.com>

ARG CADDY_VERSION=${CADDY_VERSION:-"v2.3.0-rc.1"}
ARG CADDY_PLUGINS=${CADDY_PLUGINS:-"cors,realip,expires,cache,gzip"}

# process wrapper 
RUN go get -v github.com/abiosoft/parent && \
    go install github.com/abiosoft/parent && \
    echo "GOPATH: $GOPATH" && \
    echo "PATH: $PATH" && \
    which parent

RUN echo "VERSION=${CADDY_VERSION} PLUGINS=${CADDY_PLUGINS}" && \
    VERSION=${CADDY_VERSION} PLUGINS=${CADDY_PLUGINS} ENABLE_TELEMETRY=false /bin/sh /usr/bin/caddy-builder

FROM alpine:3.12 AS runtime
MAINTAINER Michalski Luc <michalski.luc@gmail.com>

# Set build arguments
ARG VERSION
ARG BUILD
ARG NOW

# Install runtime dependencies & create runtime user
RUN apk --no-cache --no-progress add ca-certificates openssl bash nano \
    && adduser -D seoz -h /opt/seoz -s /bin/sh \
    && su seoz -c 'cd /opt/seoz; mkdir -p www logs'

# Switch to user context
USER seoz
WORKDIR /opt/seoz

# Copy the virtual environment from the previous image
COPY --from=front-builder /app/build /opt/seoz/www

# Install caddy 
COPY --from=caddy-builder /usr/bin/caddy /usr/bin/caddy

COPY Caddyfile /etc/Caddyfile
COPY --from=caddy-builder /go/bin/parent /bin/parent

# Container configuration
EXPOSE 3000 80 443 2015 
VOLUME /opt/seoz/www

# Set container labels
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

ENTRYPOINT ["/bin/parent", "caddy"]
CMD ["run", "--config=/etc/Caddyfile", "--watch"]