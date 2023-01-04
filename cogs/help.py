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
class Help(commands.Cog):
    

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(description=languague['helpdesc'])
    async def help(self,ctx):
        embed = (
        nextcord.Embed(color=0x3030FF, title=languague['help'],description=languague['helpdesc']))
        for cog in self.bot.cogs:
            for command in self.bot.get_cog(cog).get_commands():
                if not command.hidden:
                    embed.add_field(name=command.name, value=command.description)
                    
        #embed.set_image(url=imagem)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))