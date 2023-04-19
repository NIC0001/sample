FROM python:3.6

RUN set -x && \
  apt-get update && \
  apt-get install -y supervisor && \
  pip install requests && \
  pip install pytz

RUN touch /etc/supervisor/conf.d/getnodes.conf
RUN echo '[supervisord]'  >> /etc/supervisor/conf.d/getnodes.conf
RUN echo 'nodaemon=true' >> /etc/supervisor/conf.d/getnodes.conf
RUN echo '[program:getnodes]'  >> /etc/supervisor/conf.d/getnodes.conf
RUN echo 'directory=/root/src'  >> /etc/supervisor/conf.d/getnodes.conf
RUN echo 'command=/usr/local/bin/python3.6 /root/src/get-btc-nodes.py'  >> /etc/supervisor/conf.d/getnodes.conf
RUN echo 'numprocs=1'  >> /etc/supervisor/conf.d/getnodes.conf
RUN echo 'autostart=true'  >> /etc/supervisor/conf.d/getnodes.conf
RUN echo 'autorestart=true'  >> /etc/supervisor/conf.d/getnodes.conf
RUN echo 'user=root'  >> /etc/supervisor/conf.d/getnodes.conf
RUN echo 'redirect_stderr=true'  >> /etc/supervisor/conf.d/getnodes.conf
RUN echo 'stdout_logfile=/root/log/getnodes.log'  >> /etc/supervisor/conf.d/getnodes.conf

CMD /usr/bin/supervisord
