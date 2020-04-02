import re
import os
import json
import discord
from db.mongo import read_resources, read_resources_where, create_resource, update_resource, delete_resource
from discord.ext import commands
from lib.converters import *

class Resources(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(help="Adds a resource of the given type.")
    async def add(self, ctx, resource_type, *args):
        role = discord.utils.find(lambda r: r.name == f"{resource_type} Czar", ctx.author.roles)
        if role:
            resource = create_resource(resource_type, convert_arg_to_dict(args))
            if resource:
                await ctx.send(f"{resource_type} added!")
            else:
                await ctx.send(f"Something went wrong...")
        else:
            await ctx.send("Unauthorized action.")

    @commands.command(help='''
    Updates a resource of the given type.
    At the moment only one querey is allowed, but all attributes can be updated, and new attributes can be added.

    Syntax:
        !! update <Resource> where <attribute>=<value> : <attribute to update 1>=<new value 1>, <attribute to update 2>=<new value 2>, ...

    Sample input:
        !!update Birb where name=fiona the birb : description=a kind and gentle birb, eating_habits=kills for fun
    ''')
    async def update(self, ctx, resource_type, where, *args):
        role = discord.utils.find(lambda r: r.name == f"{resource_type} Czar", ctx.author.roles)

        if not role:
            await ctx.send("Unauthorized action.")
            return

        # seperate by :
        sep_vals = " ".join(args).split(" : ")
        query = sep_vals[0].split(" ")
        args = sep_vals[1].split(" ")

        resource = update_resource(resource_type, convert_arg_to_dict(query), convert_arg_to_dict(args))
        if resource:
            await ctx.send(f"{resource_type} updated!")
        else:
            await ctx.send(f"Something went wrong...")

    @commands.command(help="Fetches a list of resources.")
    async def view(self, ctx, resource_type):
        _resources = read_resources(resource_type)
        _resources = cursor_to_string(_resources)
        if _resources:
            await ctx.send(f"{resource_type}s:")
            await ctx.send(_resources)
        else:
            await ctx.send(f"No {resource_type}s yet!")

    @commands.command(help="Fetches a list of resources.")
    async def viewGroup(self, ctx, resource_type, *args):
        if "=" not in " ".join(args):
            await ctx.send(f"No query provided...")
            return
        args = convert_arg_to_dict(args)
        _resources = read_resources_where(resource_type, args)
        _resources = cursor_to_string(_resources)
        if _resources:
            await ctx.send(_resources)
        else:
            await ctx.send(f"No {resource_type}s yet!")

    @commands.command(help="Removes a reource from the corresponding resource type")
    async def remove(self, ctx, resource_type, *args):
        args = " ".join(args)
        if not args.startswith("where "):
            return "Syntax error"
        args = args[len("where "):]
        args = convert_arg_to_dict(args.split(" "))
        removed = delete_resource(resource_type, args)
        await ctx.send(f"{removed} {resource_type} deleted.")
