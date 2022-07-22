import os

import ujson as json
from dhooks import Embed, File, Webhook
from dotenv import load_dotenv

from api.homelabsales import hls_scrape
from utils.utils import crimson

load_dotenv()
hls = os.getenv("hls_webhook_url")


class HomeLab:
    @staticmethod
    def hls_monitor():
        """
        If the file exists and is not empty, then send a discord webhook with the data from the reddit API. If the file does
        not exist, then create the file and dump the data from the reddit API into it
        """

        # call API
        # patch-notes channel
        saved_json = "hls_old.json"
        responseJSON = hls_scrape()

        basetree = responseJSON["data"][0]

        title = basetree["title"]
        # thumbnail = basetree["thumbnail_url"]
        url_path = basetree["url_path"]
        author = basetree["author"]
        # description = basetree["selftext"]
        flair = basetree["flair"]
        full_url = "https://www.reddit.com" + url_path

        # check if saved_json exists and check if it is empty
        if os.path.exists(saved_json) and not saved_json:
            with open(saved_json, "r") as f:
                # update saved_json
                hook = Webhook(hls)

                embed = Embed(
                    title="HomeLab Sales",
                    description=f"[{title}]({full_url})\n\n author: {author}",
                    color=crimson,
                    timestamp="now",  # sets the timestamp to current time
                )
                embed.set_footer(text="HLS")
                # embed.set_image(url=thumbnail)
                file = File("./assets/images/hls_logo.png", name="hls_logo.png")
                embed.set_thumbnail(url="attachment://hls_logo.png")

                hook.send(embed=embed, file=file)
                with open(saved_json, "w") as updated:
                    json.dump(responseJSON, updated, ensure_ascii=False)

                updated.close()

        else:
            # print("No saved_json")
            with open(saved_json, "w") as f:
                json.dump(responseJSON, f, ensure_ascii=False)
            f.close()
