import discord
from discord.ext import commands
import tic_tac_toe

TOKEN = ''

def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    # client = discord.Client(intents=intents)

    bot = commands.Bot(command_prefix='$', intents=intents)



    @bot.command()
    async def tictac(ctx):
        if len(ctx.message.mentions) != 1:
            await ctx.send(f'Please mention another person that is not a bot and try again')
            return
        await tic_tac_toe.tic_tac(ctx, bot)

    bot.run(TOKEN)


run_bot()

