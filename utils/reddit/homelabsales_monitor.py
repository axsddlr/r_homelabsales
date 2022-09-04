import os

import pyntfy
import ujson as json
from dhooks import Embed, File, Webhook

from api.homelabsales import hls_scrape
from utils.utils import crimson, flatten

with open('./config.json') as f:
    data = json.load(f)
    hls = data["hls_webhook_url"]
    flair = data["flair"]


class HomeLab:
    @staticmethod
    def hls_monitor_discord(flair=flair):
        """
        If the file exists and is not empty, then send a discord webhook with the data from the reddit API. If the file does
        not exist, then create the file and dump the data from the reddit API into it
        """

        # Calling the hls_scrape function from the api.homelabsales module.
        responseJSON = hls_scrape()

        title = responseJSON["data"][0]["title"]

        new_entry = responseJSON["data"][0]
        new_title = new_entry["title"]
        # thumbnail = new_entry["thumbnail_url"]
        new_url_path = new_entry["url_path"]
        new_author = new_entry["author"]
        # description = new_entry["selftext"]
        # flair = new_entry["flair"]
        new_full_url = new_url_path

        # create file named hls.json
        if not os.path.exists("./hls.json"):
            with open("./hls.json", "w") as f:
                json.dump(responseJSON, f)

        with open("./hls.json") as f:
            data = json.load(f)
            res = flatten(data, "", None)
        check_file_json = res["data"][0]["title"]

        if title != check_file_json:
            hook = Webhook(hls)

            embed = Embed(
                title="HomeLab Sales",
                description=f"[{title}]({new_full_url})\n\n author: {new_author}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text=f"HLS ({flair})")
            # embed.set_image(url=thumbnail)
            file = File("./assets/images/hls_logo.png", name="hls_logo.png")
            embed.set_thumbnail(url="attachment://hls_logo.png")

            hook.send(embed=embed, file=file)

            # create a new file and dump the data from old_entry into it
            with open("./hls.json", "w") as f:
                json.dump(responseJSON, f)
        # if the new entry is the same as the last entry in the json file, then do nothing
        elif title == check_file_json:
            return

    @staticmethod
    def hls_notifications():
        # Calling the hls_scrape function from the api.homelabsales module.
        responseJSON = hls_scrape()

        title = responseJSON["data"][0]["title"]

        new_entry = responseJSON["data"][0]
        new_title = new_entry["title"]
        # thumbnail = new_entry["thumbnail_url"]
        new_url_path = new_entry["url_path"]
        new_author = new_entry["author"]
        # description = new_entry["selftext"]
        # flair = new_entry["flair"]
        new_full_url = new_url_path

        # create file named hls.json
        if not os.path.exists("./hls.json"):
            with open("./hls.json", "w") as f:
                json.dump(responseJSON, f)

        with open("./hls.json") as f:
            data = json.load(f)
            res = flatten(data, "", None)
        check_file_json = res["data"][0]["title"]

        if title != check_file_json:
            notif = pyntfy.Notification('r_hls', "", title=title)
            notif.add_action(pyntfy.actions.ViewAction('Link', new_full_url))
            notif.send()

            # create a new file and dump the data from old_entry into it
            with open("./hls.json", "w") as f:
                json.dump(responseJSON, f)
        # if the new entry is the same as the last entry in the json file, then do nothing
        elif title == check_file_json:
            return
