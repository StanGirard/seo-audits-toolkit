FROM mhart/alpine-node:14
MAINTAINER Michalski Luc <michalski.luc@gmail.com>

WORKDIR /app
COPY package.json yarn.lock ./

RUN yarn install

COPY . .

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

CMD  ["yarn", "start"]
