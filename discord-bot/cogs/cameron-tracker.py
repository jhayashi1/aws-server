from discord.ext import commands
from datetime import datetime, time
import os
import discord
import dotenv

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
        if author.name == USERNAME and author.status == discord.Status.offline:
            num_times = int(os.environ['CAMERON']) + 1
            os.environ['CAMERON'] = str(num_times)
            dotenv.set_key(dotenv.find_dotenv(), 'CAMERON', os.environ['CAMERON'])

            return

async def setup(bot):
    await bot.add_cog(CameronTracker(bot))
