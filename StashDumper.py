import discord
from discord.ext import commands


intents = discord.Intents.default()
prefix = "#"
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.load_extension('meme')


bot.run('')
