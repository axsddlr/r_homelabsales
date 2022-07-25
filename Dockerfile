FROM python:3.8-alpine
LABEL maintainer="Andre Saddler <contact@rehkloos.com>"

LABEL build_date="2021-05-23"
RUN apk update && apk upgrade
RUN apk add --no-cache git make build-base linux-headers

WORKDIR /hls_bot

COPY . .
COPY /config.example.json /hls_bot/config.json
COPY /assets/hls_old.json /hls_bot/hls_old.json
RUN touch /hls_bot/hls.json

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
