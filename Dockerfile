FROM python:3.9.5-slim-buster AS build

RUN mkdir -p /hls_bot

WORKDIR /hls_bot

RUN apt-get update && \
    apt-get install -y --no-install-recommends git gcc build-essential python-dev -y

COPY requirements.txt .
RUN pip install --no-cache-dir  -r requirements.txt

FROM python:3.9.5-slim-buster AS final
WORKDIR /hls_bot
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .

CMD ["python3", "bot.py"]
