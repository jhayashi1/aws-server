from discord.ext import commands
from datetime import datetime, time
import os
import discord

USERNAME = 'gaymera'

class CameronTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Number of times Cameron sends a message while invisible')
    async def cameron(self, ctx):
        num_times = os.environ['CAMERON']
        await ctx.send(f"Cameron has sent {num_times} messages as a ghost since 09/05/2023")

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        if author == USERNAME and author.status == discord.Status.offline:
            num_times = int(os.environ['CAMERON'])
            os.environ['CAMERON'] = num_times + 1
            return
        

async def setup(bot):
    await bot.add_cog(CameronTracker(bot))
