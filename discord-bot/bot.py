import asyncio
import discord
import os
from discord.ext import commands

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
token = open("token.txt").read()

intents = discord.Intents.all()
intents.messages = True

class MyBot(commands.Bot):
    async def setup_hook(self):
        bot.remove_command('help')
        await load_extensions()
        print("extensions loaded")

async def load_extensions():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            await bot.load_extension('cogs.' + name)

bot = MyBot(command_prefix=',', intents=intents)
bot.run(token)
