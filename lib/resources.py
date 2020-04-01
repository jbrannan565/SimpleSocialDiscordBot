import re
import os
import json
import discord
from db.mongo import read_resources, read_resources_where, create_resource, update_resource, delete_resource
from discord.ext import commands

def convert(args):
    ret = {}

    args = " ".join(args)
    args = args.split(', ')

    for a in args:
        a = a.split('=')
        ret[a[0]] = a[1]
    
    return ret

def dict_to_string(resource):
    _resource = ""
    for (key,val) in resource.items():
        if key == "_id" or key == "last_update":
            continue
        _resource += f"\t{key}: {val}\n"
    return _resource

def cursor_to_string(cursor):
    _ret = ""
    for c in cursor:
        _ret += dict_to_string(c)
        _ret += "\n"
    return _ret


class Resources(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(help="Adds a resource of the given type.")
    async def add(self, ctx, resource_type, *args):
        role = discord.utils.find(lambda r: r.name == f"{resource_type} Czar", ctx.author.roles)
        if role:
            resource = create_resource(resource_type, convert(args))
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

        resource = update_resource(resource_type, convert(query), convert(args))
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
        args = convert(args)
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
        args = convert(args.split(" "))
        removed = delete_resource(resource_type, args)
        await ctx.send(f"{removed} {resource_type} deleted.")
