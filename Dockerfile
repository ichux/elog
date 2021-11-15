FROM python:3.8.8-buster

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

RUN apt-get update && apt-get install -y nginx supervisor netcat
RUN apt-get -y --purge autoremove && apt-get -y clean && rm -rf /var/lib/apt/lists/*

COPY customize/elog.conf /etc/nginx/sites-available/
COPY customize/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN mkdir -p /var/log/supervisor && rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/elog.conf /etc/nginx/sites-enabled/elog.conf \
    && echo "daemon off;" >> /etc/nginx/nginx.conf && chown -R www-data:www-data /var/log

WORKDIR /var/www/

COPY requirements.txt /var/www/requirements.txt

COPY . .

RUN pip install --no-index --no-cache-dir --disable-pip-version-check \
  --find-links=./libraries -r ./requirements.txt setuptools wheel uwsgi

EXPOSE 5000 9001

ENTRYPOINT ["sh", "./entrypoint.sh"]
