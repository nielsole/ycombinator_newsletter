FROM alpine:3.5
RUN apk update
RUN apk add python3 -y
ADD ./code /code
RUN pip3 install -r /code/requirements.txt
ADD ./hn-cron /etc/crontabs/root
RUN mkdir /data
CMD tail -f /dev/null
