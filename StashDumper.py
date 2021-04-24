import discord
from discord.ext import commands
import os
import dotenv


dotenv.load_dotenv()
intents = discord.Intents.default()
prefix = os.getenv("PREFIX")
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.load_extension('meme')


@bot.event
async def on_ready():
    print(f'{bot.user} has successfully connected to Discord!\nPing: {round(bot.latency * 1000, 2)}ms. My prefix is {prefix}')
    activity_type = discord.ActivityType.playing
    await bot.change_presence(activity=discord.Activity(type=activity_type, name=f"{prefix}help or {prefix}about"))

bot.run(os.getenv("TOKEN"))
