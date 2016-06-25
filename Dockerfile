FROM ubuntu:14.04
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install rsyslog -y
RUN rsyslogd
RUN touch /var/log/syslog
#RUN touch /var/log/cron.log
ADD ./code /code
RUN pip3 install -r /code/requirements.txt
ADD ./hn-cron /etc/cron.d/hn
RUN mkdir /data
CMD cron -L15 && tail -f /var/log/syslog
