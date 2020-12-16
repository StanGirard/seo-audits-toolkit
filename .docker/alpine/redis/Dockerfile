ARG REDIS_VERSION=${REDIS_VERSION:-"6"}

FROM redis:${REDIS_VERSION}-alpine
MAINTAINER Luc Michalski <michalski.luc@gmail.com>

ARG REDIS_LOG_PREFIX_PATH=${REDIS_LOG_PREFIX_PATH:-"/var/log/redis"}

RUN mkdir -p ${REDIS_LOG_PREFIX_PATH} && \
    chown redis ${REDIS_LOG_PREFIX_PATH}
