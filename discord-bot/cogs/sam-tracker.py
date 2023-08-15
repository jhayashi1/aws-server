from discord.ext import commands
from datetime import datetime, time
import os
import discord

USERNAME = 'hotwire12'

class SamTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Number of times Sam gets online during work hours')
    async def sam(self, ctx):
        num_times = os.environ['SAM']
        await ctx.send("Sam slacked off at work and gotten on discord " + str(num_times) + " times since 08/15/2023")

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        now = datetime.now()
        #Check username -> time greater than 9am and less than 5pm -> day is not weekend -> current status is online -> previous status is not online
        if before != USERNAME or now.time() < time(9) or now.time() > time(17) or now.weekday() >= 5 or after.status != discord.Status.online or before.status == discord.Status.online:
            return

        num_times = int(os.environ['SAM'])
        os.environ['SAM'] = num_times + 1
        

async def setup(bot):
    await bot.add_cog(SamTracker(bot))