FROM ghcr.io/home-assistant/base:3.24

ARG BUILD_VERSION
ARG BUILD_ARCH

RUN apk add --no-cache \
    python3 \
    py3-matplotlib \
    py3-paho-mqtt \
    py3-websockets \
    font-dejavu

COPY rootfs /

RUN chmod 0755 \
    /etc/services.d/gmc/run \
    /etc/services.d/gmc-reports/run \
    /usr/local/bin/gmc_bridge.py \
    /usr/local/bin/gmc_report_server.py \
    /usr/local/bin/gmc_runtime_env.py

LABEL \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="app" \
    io.hass.arch="${BUILD_ARCH}"
