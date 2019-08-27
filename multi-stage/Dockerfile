
FROM ubuntu:bionic AS Stage0

COPY ./hello_world_tool /opt/hello_world_tool

# CMake version 3.14.5
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://cmake.org/files/v3.14/cmake-3.14.5-Linux-x86_64.sh && \
    /bin/sh /var/tmp/cmake-3.14.5-Linux-x86_64.sh --prefix=/usr/local --skip-license && \
    rm -rf /var/tmp/cmake-3.14.5-Linux-x86_64.sh

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        g++ \
        make \
        wget && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/build_hello_world_tool && cd /opt/build_hello_world_tool && cmake -DCMAKE_INSTALL_PREFIX=/opt/hello_install/ -DCMAKE_INSTALL_RPATH=/usr/local/lib/ /opt/hello_world_tool/ && \
    cmake --build /opt/build_hello_world_tool --target install -- -j$(nproc)

RUN mkdir -p /opt/openssl_build && wget -q -nc --no-check-certificate -P /opt/openssl_build https://www.openssl.org/source/openssl-1.1.1c.tar.gz && \
    mkdir -p /opt/openssl_build && tar -x -f /opt/openssl_build/openssl-1.1.1c.tar.gz -C /opt/openssl_build -z && \
    cd /opt/openssl_build/openssl-1.1.1c && \
    ./config --prefix=/opt/openssl_install -Wl,-rpath=/usr/local/lib && \
    make -j && \
    make install -j && \
    cd -

FROM ubuntu:bionic AS Stage1

COPY --from=Stage0 /opt/hello_install/ /usr/local/

COPY --from=Stage0 /opt/openssl_install/ /usr/local/

ENTRYPOINT ["hello_world_tool"]