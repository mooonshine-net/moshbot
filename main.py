import discord
from discord.ext import commands
import secrets
import asyncio

client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0} seconds'.format(round(client.latency, 3)))

@bot.command()
async def shutdown(ctx, args: int):
    member = ctx.author
    if args != null:
        if ctx.message.author.server_permission.administrator:
            try:
                asyncio.wait(args)
            except:
                await ctx.send("You may only use an Integer as an argument!")

def checkperms(member, permission):

client.run(secrets.token)