# -*- coding: utf-8 -*-
from nextcord.ext import commands
import nextcord
import asyncio,json
from nextcord.ext.commands import clean_content
import os
def getconfig():
    if os.path.exists("config.json"):
        with open('config.json') as f:
            global config
            config=json.load(f)

    with open(f'langs/{config.get("languague")}.json') as f:
        global languague
        languague= json.load(f)

getconfig()
class Ping(commands.Cog):
    """Commands for providing tips about using the bot."""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(description=languague['pingdesc'])
    async def ping(self,ctx):
        await ctx.send(f"{languague['pingtext']} {self.bot.latency} ms")

def setup(bot):
    bot.add_cog(Ping(bot))