import re
import os
import json
import discord
from discord.ext import commands

def convert(args):
    ret = {}

    args = " ".join(args)
    args = args.split(', ')

    for a in args:
        a = a.split('=')
        ret[a[0]] = a[1]
    
    return ret

class Resources(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello {0.name}'.format(ctx.author.name))

    async def add_resource(self, resource_type, arguments):
        resource_file = f"resources/{resource_type}"
        with open(resource_file, 'a+') as f:
            f.write(json.dumps(arguments) + "\n")
            f.close()

    async def get_resources(self, resource_type):
        resource_file = f"resources/{resource_type}"
        if not os.path.isfile(resource_file):
            return f"No {resource_type}s yet!"

        with open(resource_file, 'r') as f:
            content = f.readlines()
            f.close()

        json_content = [json.loads(x.strip()) for x in content]

        if len(json_content) == 0:
            return f"No {resource_type}s yet!"

        _resources = f"{resource_type}s:\n"
        for j in json_content:
            for (key, val) in j.items():
                _resources += f"\t{key}: {val}\n"
            _resources += f"\n"

        return _resources

    @commands.command(help="Adds a resource of the given type.")
    async def add(self, ctx, resource_type, *args):
        role = discord.utils.find(lambda r: r.name == f"{resource_type} Czar", ctx.author.roles)
        if role:
            await self.add_resource(resource_type, convert(args))
            await ctx.send(f"{resource_type} added!")
        else:
            await ctx.send("Unauthorized action.")

    @commands.command(help="Fetches a list of resources.")
    async def view(self, ctx, resource_type):
        _resources = await self.get_resources(resource_type)
        await ctx.send(_resources)

    async def remove_resource(self, resource_type, args):
        args = " ".join(args)
        if not args.startswith("where "):
            return "Syntax error"

        args = args[len("where"):]
        args = args.split("=")

        count = 0

        resource_file = f"resources/{resource_type}"

        if not os.path.isfile(resource_file):
            return f"No {resource_type}s yet!"

        with open(resource_file, "r") as f:
            content = f.readlines()
            
            f.close()

        if len(content) == 0:
            return f"No {resource_type}s yet!"


        with open(resource_file, "w") as f:
            json_content = [json.loads(x.strip()) for x in content]
            for line in json_content:
                if args[0] in line.keys() and line[args[0]] != args[1]:
                    f.write(json.dumps(line))
                else:
                    count += 1
            if count == 1:
                return f"{count} {resource_type} removed."
            return f"{count} {resource_type}s removed."

    @commands.command(help="Removes a reource from the corresponding resource type")
    async def remove(self, ctx, resource_type, *args):
        removed = await self.remove_resource(resource_type, args)
        await ctx.send(removed)
