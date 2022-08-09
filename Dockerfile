FROM python:3.9.5-slim-buster AS build

RUN mkdir -p /hls_bot

WORKDIR /hls_bot

RUN apt-get update && \
    apt-get install -y --no-install-recommends git gcc build-essential python3-dev apt-utils

COPY requirements.txt .
RUN pip install --no-cache-dir  -r requirements.txt

FROM python:3.9.5-slim-buster AS final
WORKDIR /hls_bot
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .

RUN echo '{"status":200,"data":[{"title":"","url_path":"","author":"","flair":""}]}' > /hls_bot/hls.json

RUN chmod -R 777 .

CMD ["python", "bot.py"]
