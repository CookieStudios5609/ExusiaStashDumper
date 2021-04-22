import discord
from discord.ext import commands
import os
import dotenv


dotenv.load_dotenv()
intents = discord.Intents.default()
prefix = os.getenv("PREFIX")
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.load_extension('meme')


bot.run(os.getenv("TOKEN"))
