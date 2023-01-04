from nextcord.ext import commands
import nextcord
import random
import os
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
    with open('gifs.json') as f:
        global gifs
        gifs= json.load(f)
getconfig()
class Ship(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description=languague['shipdesc'])
    async def ship(self, ctx, name1 :nextcord.Member,name2:nextcord.Member):
        shipnumber = random.randint(0,100)
        if 0 <= shipnumber <= 10:
            status =languague['0percent']['status'] + random.choice(languague['0percent']['values'])
            imagem=gifs['0percent'];
        elif 10 < shipnumber <= 20:
            status =languague['10percent']['status'] + random.choice(languague['10percent']['values'])
            imagem=gifs['10percent'];
        elif 20 < shipnumber <= 30:
            status =languague['10percent']['status'] + random.choice(languague['10percent']['values'])
            imagem=gifs['20percent'];
        elif 30 < shipnumber <= 40:
            status =languague['10percent']['status'] + random.choice(languague['10percent']['values'])
            imagem=gifs['30percent'];
        elif 40 < shipnumber <= 60:
            status =languague['41-59percent']['status'] + random.choice(languague['41-59percent']['values'])
            imagem=gifs['41-59percent'];
        elif 60 < shipnumber <= 70:
            status = languague['60percent']['status'] + random.choice(languague['60percent']['values'])
            imagem=gifs['60percent'];
        elif 70 < shipnumber <= 80:
            status = languague['70percent']['status'] + random.choice(languague['70percent']['values'])
            imagem=gifs['70percent'];
        elif 80 < shipnumber <= 90:
            status =languague['80percent']['status'] + random.choice(languague['80percent']['values'])
            imagem=imagem=gifs['80percent'];
        elif 90 < shipnumber <= 100:
            status = languague['91-100percent']['status'] + random.choice(languague['91-100percent']['values'])
            imagem=gifs['91-100percent'];
        if shipnumber <= 33:
            shipColor = 0xF80F0F
        elif 33 < shipnumber < 66:
            shipColor = 0x096FFF
        else:
            shipColor = 0x9B04D6

        embed = (
            nextcord.Embed(color=shipColor, title=languague['lovetest'],\
            description="**{0.mention}** e **{1.mention}** {2}".format(name1, name2, random.choice([":sparkling_heart:",":white_heart:",":heart_exclamation:",":heartbeat:",":heartpulse:",":hearts:",":blue_heart:",":green_heart:",":purple_heart:",":revolving_hearts:",":yellow_heart:",":two_hearts:"]))))
        embed.add_field(name=languague['loveresult'], value=f"{shipnumber}%", inline=True)
        embed.add_field(name="Status:", value=(status), inline=False)
        embed.set_image(url=imagem)
        await ctx.send(embed=embed)
 

def setup(bot):
    bot.add_cog(Ship(bot))