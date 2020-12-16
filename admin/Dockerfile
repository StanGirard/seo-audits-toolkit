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

FROM abiosoft/caddy:builder AS caddy-builder 
MAINTAINER Michalski Luc <michalski.luc@gmail.com>

ARG CADDY_VERSION=${CADDY_VERSION:-"1.0.3"}
ARG CADDY_PLUGINS="filemanager,cors,realip,expires" 

# process wrapper 
RUN go get -v github.com/abiosoft/parent
RUN VERSION=${CADDY_VERSION} PLUGINS=${CADDY_PLUGINS} ENABLE_TELEMETRY=false /bin/sh /usr/bin/builder.sh

FROM alpine:3.12 AS runtime
MAINTAINER Michalski Luc <michalski.luc@gmail.com>

# Set build arguments
ARG VERSION
ARG BUILD
ARG NOW

# Install runtime dependencies & create runtime user
RUN apk --no-cache --no-progress add ca-certificates openssl \
    && adduser -D seoz -h /opt/seoz -s /bin/sh \
    && su seoz -c 'cd /opt/seoz; mkdir -p www logs'

# Switch to user context
USER seoz
WORKDIR /opt/seoz

# Copy the virtual environment from the previous image
COPY --from=front-builder /opt/seoz/build /opt/seoz/www

# Install caddy 
COPY --from=caddy-builder /install/caddy /usr/bin/caddy

# Validate install 
RUN /usr/bin/caddy -version
RUN /usr/bin/caddy -plugins

COPY Caddyfile /etc/Caddyfile
COPY --from=builder /go/bin/parent /bin/parent

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
CMD ["--conf", "/etc/Caddyfile", "--log", "stdout", "--agree=true"]
