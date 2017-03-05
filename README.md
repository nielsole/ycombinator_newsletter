[![Build Status](https://drone.niels-ole.com/api/badges/nielsole/ycombinator_newsletter/status.svg)](https://drone.niels-ole.com/nielsole/ycombinator_newsletter)
# Hacker News Newsletter
Sometimes missing out on some of the topstories of Hacker News?

## Custom mail sending
Change the function `send_simple_message` in `midnight.py` to send emails according to your needs. (E.g. sending via Mailgun)
The default expects an `API_KEY` to be imported from `credentials.py`.

## When to send out the newsletter?
The times are set in `hn-cron` (UTC)

## Build Docker Image
This project can run standalone as Docker-Container.

    docker build -t nielsole/ycombinator_newsletter . no-cache=True

## Run the Container
A sample configuration is provided in the `docker-compose.yml`.

    docker-compose up -d