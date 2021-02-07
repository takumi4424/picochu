from ubuntu:20.04
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y \
      git python3 ca-certificates \
      cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /opt/pico \
 && git -C /opt/pico -c advice.detachedHead=false clone -q -b main   https://github.com/takumi4424/picoco.git \
 && git -C /opt/pico -c advice.detachedHead=false clone -q -b master https://github.com/raspberrypi/pico-sdk.git \
 && git -C /opt/pico/pico-sdk submodule update -q --init
ENV PICOCO_PATH=/opt/pico/picoco \
    PICO_SDK_PATH=/opt/pico/pico-sdk
ENV PATH=$PATH:$PICOCO_PATH/bin
