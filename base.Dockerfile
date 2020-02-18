FROM debian:buster-slim

ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y build-essential wget \
libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev \
libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev nginx supervisor

# Download, compile and install Python 3.7.6
RUN wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz \
&& tar xzf Python-3.7.6.tgz && cd Python-3.7.6 \
&& ./configure --enable-optimizations \
&& make altinstall && cd .. && rm -rf Python-3.7.6/ Python-3.7.6.tgz

RUN apt-get -y --purge autoremove && apt-get -y clean && rm -rf /var/lib/apt/lists/*
CMD ["bash"]