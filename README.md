# Hacker News Newsletter
Sometimes missing out on some of the topstories of Hacker News?

#Usage
Run crawl.sh periodically (e.g. every hour)
```
docker-compose run cron /code/crawl.sh
```
Run midnight.sh periodically(e.g. once daily)
```
docker-compose run cron /code/midnight.sh
```
You need to create a file named credentials.py which contains your mailgun credentials API_KEY and HOST.
Place the addresses you wish to distribute the newsletter to into addresses.txt one per line
