import json
import os

import discord
from discord.ext import commands


# Checking if the config.json file exists, if it does it will load the token from the file and if it doesn't it will
# exit the program.
if os.path.exists("config.json"):
    with open('config.json') as f:
        data = json.load(f)
        TOKEN = data["DISCORD_TOKEN"]
else:
    print("config.json not found")
    exit()


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def startup(self):
        await bot.wait_until_ready()
        await bot.tree.sync()
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="I smell some sales"))
        print('Sucessfully synced applications commands')
        print(f'Connected as {bot.user}')

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    print("{0} is online".format(filename[:-3]))
                except Exception as e:
                    print("{0} was not loaded".format(filename))
                    print(f"[ERROR] {e}")

        self.loop.create_task(self.startup())


bot = Bot()
# get string from config file
bot.run(TOKEN, reconnect=True)
