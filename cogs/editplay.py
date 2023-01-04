# -*- coding: utf-8 -*-
from nextcord.ext import commands
import nextcord
import os
import json
import sqlite3
import asyncio,json
from nextcord.ext.commands import clean_content
def getconfig():
    if os.path.exists("config.json"):
        with open('config.json') as f:
            global config
            config=json.load(f)

    with open(f'langs/{config.get("languague")}.json') as f:
        global languague
        languague= json.load(f)

getconfig()
donoid=config.get('ownerid')
class Editplay(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    @commands.command(description=languague['editplaydesc'])
    async def editplay(self, ctx,*,text):
        dono=config.get('ownerid')
        if int(dono) == ctx.message.author.id:
            con=sqlite3.connect(config.get('database'))
            cur= con.cursor()
            cur.execute(f'Update status set  stat="{text}" where id="1"')
            con.commit()
            await self.bot.change_presence(activity=nextcord.Game(name=text))
            await ctx.send(f"{languague['editdesc']}")
  
    
def setup(bot):
    bot.add_cog(Editplay(bot))
