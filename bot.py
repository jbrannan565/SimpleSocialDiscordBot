# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

@bot.command(name='Marx', help="Responds with a random quote from a famous communist")
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'The theory of Communism may be summed up in one sentence: Abolish all private property.'
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

class Greeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(
                f"Привет {member.name}! Welcome to {member.guild.name}, a Simple Social Club."
            )

bot.add_cog(Greeting(bot))
bot.run(TOKEN)