import nextcord
import asyncio 
import os
import random 
import string 
import sqlite3
import json
import time 
from nextcord.ext import commands
def getconfig():
    if os.path.exists("config.json"):
        with open('config.json') as f:
            global config
            config=json.load(f)

    with open(f'langs/{config.get("languague")}.json') as f:
        global languague
        languague= json.load(f)
        
getconfig()
donoid=config.get('donoid')

def get_bank(userID):
    conn = sqlite3.connect(config.get('database'))
    cursorObj = conn.cursor()
    cursor = cursorObj.execute("SELECT ID, MONEY,SHARD,LSHARD FROM bank")
    for row in cursor:
        if userID in row:
            return(round(row[1]))
    conn.commit()

def get_bank_all(userID):
    conn = sqlite3.connect(config.get('database'))
    cursorObj = conn.cursor()
    cursor = cursorObj.execute("SELECT ID, MONEY,SHARD,LSHARD FROM bank")
    for row in cursor:
        if userID in row:
            return(row[1],row[2],row[3])
    conn.commit()


def update_bank(userID,type,amount):
    conn = sqlite3.connect(config.get('database'))
    cursorObj = conn.cursor()
    if type == "money":
        cursorObj.execute(f'UPDATE bank SET MONEY = MONEY + {amount} where ID = {userID}')
    elif type == "shard":
        cursorObj.execute(f'UPDATE bank SET SHARD = SHARD + {amount} where ID = {userID}')
    else :
        cursorObj.execute(f'UPDATE bank SET LSHARD = LSHARD + {amount} where ID = {userID}')
    conn.commit()

def make_bank(userID):
    try:
        conn = sqlite3.connect(config.get('database'))
        conn.execute("CREATE TABLE IF NOT EXISTS bank (ID INT PRIMARY KEY,MONEY INT,SHARD INT,LSHARD INT);")
    except Exception as e:
        print(e)
    if get_bank(userID) is None:
        try:
            conn = sqlite3.connect(config.get('database'))
            conn.execute(f"INSERT  or IGNORE INTO bank (ID, MONEY,SHARD,LSHARD)  VALUES ({int(userID)},0,0,0 );")
            conn.commit()
        except Exception as e:
            print(e)
    


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
    
    @commands.command(hidden=True)
    async def makeall(self, ctx):
        if ctx.author.id==donoid:
            for a in self.bot.get_all_members():
                if not a.bot:
                    if a.id is not None:
                        make_bank(str(a.id))


    @commands.command(hidden=True)
    async def add(self, ctx, member:nextcord.Member,tipo:str,coins:int):
        if ctx.author.id==int(donoid):
            print(member.id,tipo,coins)
            update_bank(member.id,tipo,coins)
            

  
    @commands.command(description=languague['givedesc'])
    async def give(self, ctx, member:nextcord.Member, coins:int):
        make_bank(str(ctx.author.id))
        make_bank(str(member.id))
        if member==ctx.message.author:
            embed=nextcord.Embed(description=languague['selfgive'], color=nextcord.Colour.dark_gold())
            await ctx.send(embed=embed)
        elif coins>get_bank(ctx.author.id):
            embed=nextcord.Embed(description=languague['givemore'], color=nextcord.Colour.dark_gold())
            await ctx.send(embed=embed)         
        elif coins<0:
            embed=nextcord.Embed(description=languague['donttrydirt'], color=nextcord.Colour.dark_gold())
            await ctx.send(embed=embed)
        else:
            update_bank(ctx.author.id,'money', coins*-1)
            update_bank(member.id,'money', coins)
            gived=(languague['gived']%(member.name,coins))
            embed=nextcord.Embed(description=gived, color=nextcord.Colour.dark_gold())
            await ctx.send(embed=embed)
           

    @commands.command(description=languague['baldesc'])
    async def bal(self, ctx,member:nextcord.Member=None):
        make_bank(str(ctx.author.id))
        
        if member==None:
            unome=ctx.author.name
            money,shard,lshard=get_bank_all(ctx.author.id)
        else:
            make_bank(str(member.id))
            money,shard,lshard=get_bank_all(member.id)
            unome=member.name
        saldotexto=languague['saldotexto']
        embed=nextcord.Embed(description=f"{saldotexto} {unome} \n :small_red_triangle: **{money}**\n :small_blue_diamond:**{shard}**\n:small_orange_diamond:**{lshard}**", color=nextcord.Colour.gold())
        await ctx.send(embed=embed)


    @bal.error
    async def bal_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed=nextcord.Embed(description=languague['usernotfound'], color=nextcord.Colour.red())
            await ctx.send(embed=embed)
        else:
            raise error
    

    @commands.command(description=languague['dailydesc'])
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx): 
        make_bank(str(ctx.author.id))
        moneyD=random.randint(200, 800)
        dailycongr=(languague['dailycongr']%(moneyD))
        embed=nextcord.Embed(description=dailycongr, color=nextcord.Colour.dark_gold())
        await ctx.send(embed=embed)
        update_bank(ctx.author.id,'money', moneyD)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a=time.strftime(languague['wcountdown'], time.gmtime(error.retry_after))
            embed=nextcord.Embed(description=a, color=nextcord.Colour.dark_gold())
            await ctx.send(embed=embed)
        else:
            raise error
    @commands.command(description=languague['rankdesc'])
    async def rank(self, ctx):
        conn = sqlite3.connect(config.get('database'))
        cursorObj = conn.cursor()
        cursor=cursorObj.execute("SELECT * FROM bank ORDER BY MONEY DESC")
        counter = 0 
        top10=[]
        top=[]
        for row in cursor:
            counter += 1 
            winner=row[0]
            top10.append(f"{counter}. <@{winner}> Coins: {round(row[1])}")
            #await ctx.send(f"{counter}. {winner.name} Coins: {row[1]}")
            if counter == 10:
                break
        #des=(top10,sep='\n')
        embed=nextcord.Embed(title=f"**{ctx.guild.name} rank:**", description='\n'.join(top10), color=nextcord.Colour.dark_gold())
        await ctx.send(embed=embed)
    @commands.command(description=languague['weeklydesc'])
    @commands.cooldown(1, 604800.0, commands.BucketType.user)
    async def weekly(self, ctx): 
        moneyD=random.randint(2500, 5000)
        wcongrat=(languague['wcongrat']%(moneyD))
        await ctx.send(wcongrat)
        update_bank(ctx.author.id,'money',moneyD)
    @weekly.error
    async def weekly_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a=time.strftime(languague['wcountdown'], time.gmtime(error.retry_after)) 
            await ctx.send(a)
        else:
            raise error

def setup(bot):
    bot.add_cog(Currency(bot))
      
