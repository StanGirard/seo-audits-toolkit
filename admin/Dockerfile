FROM mhart/alpine-node:14
MAINTAINER Michalski Luc <michalski.luc@gmail.com>

WORKDIR /app
COPY package.json yarn.lock ./

RUN yarn install

COPY . .

EXPOSE 3000
VOLUME ["/app/build"]

CMD  ["yarn", "start"]
