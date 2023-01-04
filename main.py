import sys
import random
import os
import nextcord
import json
import sqlite3
from nextcord.ext import commands
from nextcord import Interaction
intents = nextcord.Intents.default()
intents.message_content = True
def getconfig():
    if os.path.exists("config.json"):
        with open('config.json') as f:
            global config
            config=json.load(f)
    else:
        data = {'prefix': '[','database': 'database.db','token': 'YOUR TOKEN HERE','languague':'en'}
        with open("config.json", "w") as file:
            json.dump(data, file)
    with open(f'langs/{config.get("languague")}.json') as f:
        global languague
        languague= json.load(f)
getconfig()
con=sqlite3.connect(config.get('database'))
cur= con.cursor()
cur.execute('Select stat FROM status')
status=cur.fetchone()[0]
bot = commands.Bot(command_prefix=config.get('prefix'), intents=intents)
bot.remove_command('help')
bcolors=['\033[95m','\033[94m','\033[96m','\033[97m','\033[93m']
ENDC = '\033[0m'
@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=status))
    print(f"bot {bot.user.name} starting")
initial_extentions = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extentions.append("cogs." + filename[:-3])
if __name__ == '__main__':
    for extention in initial_extentions:
        bot.load_extension(extention)
        print(f"Module: {random.choice(bcolors)+extention.split('.')[1]+ENDC}  loaded")
bot.run(config.get('token'))


