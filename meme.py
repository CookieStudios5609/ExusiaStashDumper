import discord
from discord.ext import commands, tasks
import asyncio
import random
from glob import glob
import os
import dotenv



class Meme(commands.Cog):
    def __init__(self, bot):
        dotenv.load_dotenv()
        self.bot = bot
        self.pics = []
        self.delay = os.getenv("DEFAULT_DELAY")
        self.auto_channel = os.getenv("DEFAULT_CHANNEL")
        self.enabled = True
        path = os.getenv("IMAGE_PATH") + "/**/*.jpg"
        for filename in glob(path, recursive=True):
            self.pics.append(filename)

    @commands.command(name='meme')
    async def manual_pic(self, ctx, chan: int, *, time: int):
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

    @manual_pic.error
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

    @commands.command(name="channel", help="Sets the channel for automatic posts. Please use the id, and not the channel name")
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
            print("Sent a photo!")
            await asyncio.sleep(float(self.delay))
        else:
            print("Automeme is disabled.")



def setup(bot):
    bot.add_cog(Meme(bot))
