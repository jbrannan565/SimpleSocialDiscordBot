#! /usr/bin/env python3
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

'''
# using decorators
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} has connected to Discord!\n'
        f'{guild.name}(id: {guild.id})!'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

client.run(TOKEN)
'''

# using a class
class SimpBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!\n')
        self.guild = discord.utils.get(self.guilds, name=GUILD)

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f"Привет {member.name}! Welcome to {self.guild.name}, a Simple Social Club."
        )

    async def on_error(self, event, *args, **kwargs):
        with open('err.log', 'a') as f:
            f.write(f"{event}: {args[0]}\n")

    async def process_command(self, request):
        request = request.strip()
        print(f"New command: {request}")

    async def on_message(self, message):
        command_start = os.getenv('COMMAND_START')
        command_start_len = len(command_start)
        
        if message.author == self.user:
            return

        # if the message starts
        if message.content.startswith(command_start):
            await self.process_command(message.content[command_start_len:])

        elif message.content == 'raise-exception':
            raise discord.DiscordException

        return

        

client = SimpBotClient()
client.run(TOKEN)