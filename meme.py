import discord
from discord.ext import commands, tasks
import asyncio
import random
from glob import glob


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pics = []
        self.delay = 80
        self.enabled = True
        for filename in glob('C:/Users/%USERNAME%/Desktop/a/**/*.jpg', recursive=True):
            self.pics.append(filename)

    @commands.command(name='something')
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
        await channel.send("A meme, from Exusia!", file=discord.File(random.choice(list(self.pics))))

    @manual_pic.error
    async def manual_pic_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Oops!", description="This command requires a channel id and a time (in seconds) to delay. Please try again.")
            await ctx.send(embed=embed)

    @commands.command(name='delay', help="Sets the delay between automatic image posts")
    async def set_delay(self, ctx, *, delay: int):
        await ctx.send(f"The current delay for automatic posts is {self.delay} seconds.")
        self.delay = int(delay)
        await ctx.send(f"The new delay for automatic posts is {self.delay} seconds.")

    @commands.command(name="auto", help="Toggles automatic posting")
    async def toggle(self, ctx):
        if self.enabled is True:
            self.enabled = False
            await ctx.send("Autoposting has been disabled.")
        else:
            self.enabled = True
        await ctx.send("Autoposting has been enabled.")

    @commands.command(name="channel", help="Sets the channel for automatic posts")
    def channel(self, ctx, *, channel):

def setup(bot):
    bot.add_cog(Meme(bot))
