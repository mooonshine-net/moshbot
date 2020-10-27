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

@client.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx, arg1: int):
    await ctx.send("Logging out in {} seconds".format(arg1))
    await asyncio.sleep(arg1)
    await ctx.send("🌄 Goodbye")
    await client.logout()

@shutdown.error
async def shutdown_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Logging out in 10 seconds")
        await asyncio.sleep(10)
        await ctx.send("🌄 Goodbye")
        await client.logout()
    elif isinstance(error, commands.BadArgument):
        await ctx.send("⚠ You may only use an Integer for an argument {}!".format(ctx.message.author.mention))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠ You dont have the required permissions to execute this command {}!".format(ctx.message.author.mention))
    else:
        await ctx.send("⚠ Something went wrong while executing this command {}!".format(ctx.message.author.mention))


client.run(secrets.token)