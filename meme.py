import discord
from discord.ext import commands
import asyncio
import random
from glob import glob


class meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pics = []
        self.delay = 80
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

    @commands.command(name='set', help="Sets the delay between automatic image posts")
    async def set_delay(self, ctx, *, delay: int):
        await ctx.send(f"The current delay for automatic posts is {self.delay} seconds.")
        self.delay = int(delay)
        await ctx.send(f"The new delay for automatic posts is {self.delay} seconds.")


def setup(bot):
    bot.add_cog(meme(bot))
