FROM buildev

ENV PYTHONUNBUFFERED 1

COPY customize/elog.conf /etc/nginx/sites-available/
COPY customize/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY customize/bashrc /root/.bashrc

WORKDIR /var/www/
COPY . .

RUN mkdir -p /var/log/supervisor && rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/elog.conf /etc/nginx/sites-enabled/elog.conf \
    && echo "daemon off;" >> /etc/nginx/nginx.conf \
    &&  pip3.7 --trusted-host pypi.python.org install -U pip setuptools uwsgi \
    && pip3.7 --trusted-host pypi.python.org install -r /var/www/elog/requirements-dev.txt \
    && chown -R www-data:www-data /var/log

EXPOSE 5000
ENTRYPOINT ["sh", "./entrypoint.sh"]