import discord
from discord.ext import commands
import secrets
import asyncio
import os

client = commands.Bot(command_prefix='$', help_command=None)


def del_line(t):
    a_file = open("bad-words.txt", "r")
    lines = a_file.readlines()
    a_file.close()

    new_file = open("bad-words.txt", "w")
    for line in lines:
        if line.strip("\n") != t:

            new_file.write(line)
    new_file.close()

def write_line(t):
    a_file = open("bad-words.txt", "a")
    a_file.write(t + "\n")
    a_file.close()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #open bad-words.txt

@client.event
async def on_message(message):
    if message.author.bot:
        return
    f = open("bad-words.txt")
    bad_words = [bad_word.strip().lower() for bad_word in f.readlines()]
    for word in bad_words:
        print(word)
    print("Recived Message: {}".format(message.content))
    if message.content.startswith("$"):
        await client.process_commands(message)
        print("skipped bad-word check")
    elif any(bad_word in message.content for bad_word in bad_words):
        repl = await message.channel.send("⚠ You cant say that here, {}!".format(message.author.mention))
        await message.delete()
        await asyncio.sleep(20)
        await repl.delete()
    else:
        await client.process_commands(message)    

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

@client.command()
@commands.has_permissions(administrator=True)
async def addswear(ctx, arg: str):
    write_line(arg)

    await ctx.send("Added {} to the the bad-word list".format(arg))
    

@addswear.error
async def addswear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠ You are Missing an argument {}!".format(ctx.message.author.mention))
    elif isinstance(error, commands.BadArgument):
        await ctx.send("⚠ You may only use an Integer for an argument {}!".format(ctx.message.author.mention))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠ You dont have the required permissions to execute this command {}!".format(ctx.message.author.mention))
    else:
        await ctx.send("⚠ Something went wrong while executing this command {}!".format(ctx.message.author.mention))
        print(str(error))


@client.command()
@commands.has_permissions(administrator=True)
async def delswear(ctx, arg: str):
    del_line(arg)
    await ctx.send("Removed {} from the bad-word list".format(arg))

@delswear.error
async def delswear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠ You are Missing an argument {}!".format(ctx.message.author.mention))
    elif isinstance(error, commands.BadArgument):
        await ctx.send("⚠ You may only use an Integer for an argument {}!".format(ctx.message.author.mention))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠ You dont have the required permissions to execute this command {}!".format(ctx.message.author.mention))
    else:
        await ctx.send("⚠ Something went wrong while executing this command {}!".format(ctx.message.author.mention))
        print(str(error))



@client.command()
async def help(ctx, cmd: str):
        embed=discord.Embed(title="Help - MoshBot", url="https://github.com/AnnikenYT/moshbot", description="For more information, check out the Github Page of the bot by clicking in the title.", color=0x3300ff)
        embed.set_author(name="AnnikenYT", url="https://github.com/AnnikenYT", icon_url="https://avatars1.githubusercontent.com/u/61291253?s=60&v=4")
        embed.add_field(name="Ping", value="Shows the bot Latency", inline=False)
        embed.add_field(name=" addswear <String>", value="(Admin only) add a word to the bad-word list", inline=False)
        embed.add_field(name="delswear <String>", value="(Admin only) remove a word from the bad-words list", inline=True)
        embed.add_field(name="shutdown [time]", value="(Admin only) turns off the bot in [time] seconds", inline=True)
        embed.add_field(name="seen [Minecraft Username]", value="(Comming Soon) Shows when a User was online last (on the minecraft server)", inline=True)
        embed.add_field(name="status [server]", value="(Comming Soon) Shows the status of the Lobby-Server / [Server]", inline=True)
        embed.set_footer(text="Moshbot")
        await ctx.send(embed=embed)

@help.error
async def delswear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="Help - MoshBot", url="https://github.com/AnnikenYT/moshbot", description="For more information, check out the Github Page of the bot by clicking in the title.", color=0x3300ff)
        embed.set_author(name="AnnikenYT", url="https://github.com/AnnikenYT", icon_url="https://avatars1.githubusercontent.com/u/61291253?s=60&v=4")
        embed.add_field(name="Ping", value="Shows the bot Latency", inline=False)
        embed.add_field(name=" addswear <String>", value="(Admin only) add a word to the bad-word list", inline=False)
        embed.add_field(name="delswear <String>", value="(Admin only) remove a word from the bad-words list", inline=False)
        embed.add_field(name="shutdown [time]", value="(Admin only) turns off the bot in [time] seconds", inline=False)
        embed.add_field(name="seen [Minecraft Username]", value="(Comming Soon) Shows when a User was online last (on the minecraft server)", inline=False)
        embed.add_field(name="status [server]", value="(Comming Soon) Shows the status of the Lobby-Server / [Server]", inline=False)
        embed.set_footer(text="Moshbot")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("⚠ You may only use an Integer for an argument {}!".format(ctx.message.author.mention))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠ You dont have the required permissions to execute this command {}!".format(ctx.message.author.mention))
    else:
        await ctx.send("⚠ Something went wrong while executing this command {}!".format(ctx.message.author.mention))
        print(str(error))
client.run(secrets.token)