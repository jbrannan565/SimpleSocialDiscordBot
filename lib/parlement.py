from discord.ext import commands

class Parlement(commands.Cog):
    def __init__(self, bot, channel_name):
        self.bot = bot
        self._last_member = None
        self.channel_name = channel_name


    @commands.command()
    async def channel_test(self, ctx):
        if ctx.channel.name != self.channel_name:
            print

