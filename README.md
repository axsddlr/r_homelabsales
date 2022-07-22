<div id="top"></div>

<br />
<div align="center">
    <img src="https://b.thumbs.redditmedia.com/I-p4xs4_haTS4zepDhqIOoHYRkVYOkCCeF8eY7SA1JU.png" alt="Logo" width="80" height="80">

<a href="https://www.reddit.com/r/homelabsales/">
  <h3 align="center">r/Homelabsales</h3>
</a>

  <p align="center">
    An Unofficial Discord Bot for Homelab Sales subreddit.
    <br />
    <br />
    <br />

  </p>
</div>


### Built With

* [Discord.py](https://discordpy.readthedocs.io/en/stable/)
* [dhooks](https://github.com/kyb3r/dhooks)
* [praw](https://praw.readthedocs.io/en/stable/)
* [APScheduler](https://apscheduler.readthedocs.io/en/3.x/)
<p align="right">(<a href="#top">back to top</a>)</p>


### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* python 3.8 +

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/axsddlr/r_homelabsales.git
   ```
2. python
   ```sh
   python -m pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

## Config
change config.example.json to config.json

```json
{
    "DISCORD_TOKEN":"<token>",
    "reddit_client_id":"<client_id>",
    "reddit_client_secret":"<client_secret>",
    "hls_webhook_url":"<webhook_url>"
}
```
<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

   ```sh
  python bot.py
   ```
<p align="right">(<a href="#top">back to top</a>)</p>

## Docker
docker-compose.yml

```yaml
---
version: '3'

services:
  hls:
    container_name: "hls_bot"
    image: "ghcr.io/axsddlr/r_homelabsales:latest"
    restart: unless-stopped
    volumes:
      - ./r_hls/config.json:/hls_bot/config.json
```
<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>




