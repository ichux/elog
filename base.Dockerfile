FROM debian:stretch-slim

RUN apt-get update && apt-get dist-upgrade && apt-get install -y build-essential checkinstall \
&& apt-get install -y wget libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev \
tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev nginx supervisor \
&& wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz \
&& tar xzf Python-3.7.6.tgz && cd Python-3.7.6 && ./configure --enable-optimizations \
&& make altinstall && cd .. && rm -rf Python-3.7.6/ Python-3.7.6.tgz \
&& apt-get -y --purge autoremove && apt-get -y clean

CMD ["bash"]
