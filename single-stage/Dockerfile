FROM ubuntu:bionic

COPY ./hello_world_tool /opt/hello_world_tool

# CMake version 3.12.3
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://cmake.org/files/v3.12/cmake-3.12.3-Linux-x86_64.sh && \
    /bin/sh /var/tmp/cmake-3.12.3-Linux-x86_64.sh --prefix=/usr/local --skip-license && \
    rm -rf /var/tmp/cmake-3.12.3-Linux-x86_64.sh

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        g++ \
        make && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/build_hello_world_tool && cd /opt/build_hello_world_tool && cmake -DCMAKE_INSTALL_PREFIX=/usr/local /opt/hello_world_tool/ && \
    cmake --build /opt/build_hello_world_tool --target install -- -j$(nproc)

ENTRYPOINT ["hello_world_tool"]