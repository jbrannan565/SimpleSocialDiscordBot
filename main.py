# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv
from lib.greeting import Greeting
from lib.resources import Resources
from lib.parlement import Parlement

# set up loggin
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')
PARLIAMENT_CHANNEL = os.getenv('PARLIAMENT_CHANNEL')

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

bot.add_cog(Greeting(bot))
bot.add_cog(Resources(bot))
bot.add_cog(Parlement(bot, PARLIAMENT_CHANNEL))
bot.run(TOKEN)