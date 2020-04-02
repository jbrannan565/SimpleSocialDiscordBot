from discord.ext import commands

class Parliament(commands.Cog):
    def __init__(self, bot, channel_name):
        self.bot = bot
        self._last_member = None
        if channel_name:
            self.channel_name = channel_name
        else:
            self.channel_name = 'voting'

    @commands.group()
    async def motion(self, ctx):
        if ctx.channel.name != self.channel_name:
            await ctx.send(
                f"Parliamentary actions can only be done inside the #{self.channel_name} channel."
                )
            return
            
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid motion argument...")

