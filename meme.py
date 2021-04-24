import discord
from discord.ext import commands, tasks
import asyncio
import random
from glob import glob
import os
import dotenv
import sys


class Meme(commands.Cog):
    def __init__(self, bot):
        dotenv.load_dotenv()
        self.bot = bot
        self.pics = []
        self.delay = os.getenv("DEFAULT_DELAY")
        self.auto_channel = os.getenv("DEFAULT_CHANNEL")
        self.enabled = True
# grab files from paths using allowed extensions key
        main_path = os.getenv("IMAGE_PATH")
        file_types_raw = os.getenv("FILE_EXTS")
        extensions = file_types_raw.split(',')
        for i, j in enumerate(extensions):
            out = main_path + "/**/*" + extensions[i]
            filename = glob(out, recursive=True)
            self.pics.extend(filename)

    @commands.command(name='meme', help="Posts an image or video in the default channel")
    async def meme(self, ctx):
        await ctx.trigger_typing()
        channel = self.bot.get_channel(int(self.auto_channel))
        await channel.send(f"A meme, from {ctx.author.display_name}!", file=discord.File(random.choice(list(self.pics))))

    @commands.command(name='memehere', help="Posts an image or video in THIS channel")
    async def meme_here(self, ctx):
        await ctx.trigger_typing()
        await ctx.send(f"A meme, from {ctx.author.display_name}!", file=discord.File(random.choice(list(self.pics))))

    @commands.command(name='memethere', help="Posts an image or video in the channel you provide")
    async def manual(self, ctx, chan: int, *, time: int):
        await ctx.trigger_typing()
        channel = self.bot.get_channel(chan)
        if time == 1:
            await ctx.send(f"Sending an image to #{channel} in {time} second.")
        elif time == 0:
            pass
        else:
            await ctx.send(f"Sending an image to #{channel} in {time} seconds")
        await asyncio.sleep(time)
        await channel.send(f"A meme, from {ctx.author.display_name}!", file=discord.File(random.choice(list(self.pics))))

    @commands.command(name='about', hidden=True)
    async def info(self, ctx):
        await ctx.trigger_typing()
        e = discord.Embed(title="StashDumper", description="An open-source media uploading bot for Exusia.")
        e.add_field(name="Status:", value=f"Python Version: **{sys.version}**\n Discord.py version: **{discord.__version__}**\n Running on **{sys.platform}**\nPing: **{round(self.bot.latency * 1000, 2)}**", inline=False)
        e.add_field(name="Need help?", value=f"Use {os.getenv('PREFIX')}help")
        e.add_field(name="Check out my source code!", value="https://github.com/CookieStudios5609/ExusiaStashDumper", inline=False)
        await ctx.send(embed=e)

    @manual.error
    async def manual_pic_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Oops!", description="This command requires a channel id and a time (in seconds) to delay. Please try again.")
            await ctx.send(embed=embed)

    @commands.command(name='delay', help="Sets the delay between automatic image posts")
    async def set_delay(self, ctx, *, delay: int):
        await ctx.send(f"The old delay for automatic posts was {self.delay} seconds.")
        self.delay = int(delay)
        await ctx.send(f"The new delay for automatic posts is {self.delay} seconds.")

    @commands.command(name="auto", help="Toggles automatic posting")
    async def toggle(self, ctx):
        if self.enabled is True:
            self.auto_memer.cancel()
            self.enabled = False
            await ctx.send("Autoposting has been disabled.")
        else:
            self.enabled = True
            self.auto_memer.start()
            await ctx.send("Autoposting has been enabled.")

    @commands.command(name="channel", help="Sets the channel id for automatic posts.")
    async def channel(self, ctx, *, channel: int):
        self.auto_channel = int(channel)
        await ctx.send(f"The channel to automatically post images to has been set to #{self.bot.get_channel(channel)}")

    @channel.error
    async def channel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Oops!",
                                  description="You must include a channel ID! Please try again.")
            await ctx.send(embed=embed)

    @set_delay.error
    async def delay_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Oops!",
                                  description="You must include a display length in seconds! Please try again.")
            await ctx.send(embed=embed)

    @tasks.loop(seconds=5)
    async def auto_memer(self):
        if bool(self.enabled):
            post_channel = self.bot.get_channel(int(self.auto_channel))
            await post_channel.send(f"An image!", file=discord.File(random.choice(list(self.pics))))
            await asyncio.sleep(float(self.delay))
        else:
            print("Automeme is disabled.")


def setup(bot):
    bot.add_cog(Meme(bot))
