import asyncio
import os
import discord
import random
from discord.ext import commands
import time
from discord.ext.commands import Bot
import _asyncio

TOKEN = #Your Token
GUILD =#Your server Name

client = discord.Client()

abusive =['fuck','shit']#any offensive word you do not want people to use

bot = Bot(command_prefix='!')

def isabusive(msg):

    for abuse in abusive:

        if abuse in msg:
            return True

    return False

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif isabusive(message.content):
        response ='Uhm Uhm! Kindly refrain from using abusive languages here :D Thanks'
        await message.channel.send(response)


    elif '...' in message.content:
        time.sleep(5)
        await message.delete()#if you use ... in a message, it will disappear automatically after 5 seconds


@bot.command(pass_context = True)
async def clear(ctx, number):
    mgs = [] #Empty list to put all the messages in the log
    number = int(number) #Converting the amount of messages to delete to an integer
    async for x in client.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)

    await client.delete_messages(mgs)


client.run(TOKEN)


