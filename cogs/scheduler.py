import os
import pathlib
from enum import Enum

import discord
import requests
from discord import app_commands
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.reddit.homelabsales_discord import HomeLab


class Scheduer(commands.Cog):

    def __init__(self, bot):
        """
        The function is called when the bot is ready, and it adds a job to the scheduler that runs the hls_monitor function
        every 15 seconds

        :param bot: the bot object
        """
        self.bot = bot
        self.hls = HomeLab()
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 200})

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = self.scheduler

        # add jobs for scheduler

        # valorant news monitor
        scheduler.add_job(self.hls.hls_monitor, "interval", seconds=15)

        # starting the scheduler
        scheduler.start()


async def setup(bot):  # set async function
    await bot.add_cog(Scheduer(bot))  # Use await
