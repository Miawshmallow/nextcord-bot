import nextcord
import sys
import traceback
import logging
import json
from nextcord.ext import commands
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
class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_listener(self.on_command_error, "on_command_error")

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return  # Don't interfere with custom error handlers

        error = getattr(error, "original", error)  # get original error

        if isinstance(error, commands.CommandNotFound):
            comandonotfound=(languague['comandonotfound']%(self.bot.command_prefix))
            return await ctx.send(comandonotfound)

        if isinstance(error, commands.CommandError):
            erroexecutando=(languague['erroexecutando']%(ctx.command.name,str(error)))
            return await ctx.send(erroexecutando)

        await ctx.send(languague['erroinesperado'])
        logging.warn("Ignoring exception in command {}:".format(ctx.command))
        logging.warn("\n" + "".join(
            traceback.format_exception(
                type(error), error, error.__traceback__)))

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))