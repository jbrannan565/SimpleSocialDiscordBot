from discord.ext import commands
from db.parliament import ParliamentDB
from lib.converters import *

class Parliament(commands.Cog):
    def __init__(self, bot, channel_name):
        self.bot = bot
        self._last_member = None
        if channel_name:
            self.channel_name = channel_name
        else:
            self.channel_name = 'voting'
        self.db = ParliamentDB()

    @commands.group()
    async def motion(self, ctx):
        if ctx.channel.name != self.channel_name:
            await ctx.send(
                f"Parliamentary actions can only be done inside the #{self.channel_name} channel."
                )
            return
            
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid motion argument...")

    '''
    VIEW COMMAND GROUP
    '''
    @motion.group()
    async def view(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid view argument...")

    @view.command()
    async def tabled(self, ctx):
        tabled = self.db.read_tabled()
        tabled = cursor_to_string(tabled)
        tabled = "Tabled Motions:\n" + tabled
        await ctx.send(tabled)

    @view.command()
    async def pending(self, ctx):
        pending = self.db.read_pending()
        pending = cursor_to_string(pending)
        pending = "Pending Motions:\n" + pending
        await ctx.send(pending)

    @view.command()
    async def laws(self, ctx):
        laws = self.db.read_laws()
        laws = cursor_to_string(laws)
        laws = "Laws:\n" + laws
        await ctx.send(laws)

    @view.command()
    async def closed(self, ctx):
        closed = self.db.read_closed()
        closed = cursor_to_string(closed)
        closed = "Closed Motions:\n" + closed 
        await ctx.send(closed)

    
    @view.command()
    async def called(self, ctx, name):
        called = self.db.read_by_name(name)
        called = cursor_to_string(called)
        if called:
            await ctx.send(called)
        else:
            await ctx.send("No motion by that name.")
    '''
    END VIEW COMMAND GROUP
    '''

    @motion.command()
    async def bring(self, ctx, name, description):
        num_created = self.db.create(name, description)
        if num_created:
            await ctx.send(f"Motion '{name}' created.")
        else:
            await ctx.send("Something went wrong...")


    @motion.command()
    async def table(self, ctx, name):
        if self.db.table(name):
            await ctx.send(f"Motion '{name}' tabled.")
        else:
            await ctx.send(f"Something wend wrong...")

    @motion.command()
    async def untable(self, ctx, name):
        if self.db.untable(name):
            await ctx.send(f"Motion '{name}' tabled.")
        else:
            await ctx.send(f"Something wend wrong...")
    
    @motion.command()
    async def amend(self, ctx, name, amendment):
        if self.db.amend(name, amendment):
            await ctx.send(f"Motion '{name}' amended.")

            amended = self.db.read_by_name(name)
            amended = cursor_to_string(amended)

            if amended:
                await ctx.send(amended)
            return

        await ctx.send(f"Something wend wrong...")

    @motion.command()
    async def legislate(self, ctx, name):
        if self.db.legislate(name):
            await ctx.send(f"Motion '{name}' signed into law.")
        else:
            await ctx.send(f"Something wend wrong...")

    @motion.command()
    async def close(self, ctx, name):
        if self.db.close(name):
            await ctx.send(f"Motion '{name}' closed.")
        else:
            await ctx.send(f"Something wend wrong...")