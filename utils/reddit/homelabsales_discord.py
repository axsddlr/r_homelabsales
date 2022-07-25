import os
import shutil

import ujson as json
from deepdiff import DeepDiff
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
        If the file exists and is not empty, then send a discord webhook with the data from the reddit API. If the
        file does not exist, then create the file and dump the data from the reddit API into it
        """
        responseJSON = hls_scrape()

        basetree = responseJSON["data"][0]

        title = basetree["title"]
        url_path = basetree["url_path"]
        author = basetree["author"]
        # flair = basetree["flair"]

        file1 = "./hls.json"
        file2 = "./hls_old.json"

        if not os.path.exists(file1) or os.stat(file1).st_size == 0:
            with open(file1, "w") as f:
                json.dump(responseJSON, f)
        elif not os.path.exists(file2):
            shutil.copy("./assets/hls_old.json", "./hls_old.json")
        else:
            # Opening the file and loading the data from the file into a variable.
            with open(file1, "r") as f1:
                data1 = json.load(f1)
            with open(file2, "r") as f2:
                data2 = json.load(f2)
            # Checking if the data in the two files are the same. If they are not the same, it will send a discord
            # webhook.
            if DeepDiff(data1, data2) != {}:
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
                shutil.copy(file1, file2)
                # Closing the file.
                f1.close()
                f2.close()
            # If the data from file1 and file2 are the same, then do nothing.
            else:
                pass
