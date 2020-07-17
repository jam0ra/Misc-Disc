import discord
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Creates event within a cog, similar to @client.event()
    @commands.Cog.listener()
    async def on_ready(self):
        print("Example Bot is ready!")

    # Creates command within a cog, similar to @client.command()
    @commands.command()
    async def marco(self, context):
        await context.send("Polo!")

def setup(client):
    client.add_cog(Example(client))
