import os

import ujson as json
from dhooks import Embed, File, Webhook

from api.homelabsales import hls_scrape
from utils.utils import crimson

with open('./config.json') as f:
    data = json.load(f)
    hls = data["hls_webhook_url"]


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

        # if saved_json does not exist, create it
        if not os.path.exists(saved_json):
            with open(saved_json, "w") as f:
                json.dump(responseJSON, f)
        # if saved_json exists, read it
        else:
            with open(saved_json, "r") as f:
                old_responseJSON = json.load(f)
            # if the old_responseJSON is not the same as the responseJSON, then send a webhook
            if old_responseJSON != responseJSON:
                with open(saved_json, "w") as f:
                    json.dump(responseJSON, f)
                # send webhook
                if flair != "US-E":
                    # print("not patch notes")
                    return
                elif flair == "US-E":
                    # print("False")
                    hook = Webhook(hls)

                    embed = Embed(
                        title="HomeLab Sales",
                        description=f"[{title}]({url_path})\n\n author: {author}",
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
                return
