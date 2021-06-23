import asyncio
import logging
import os
import discord
import random
from discord.ext import commands
import time
import _asyncio
import keep_alive
import pyjokes
import random
import sqlite3
import wikipedia
import requests
import bs4
import music_player


TOKEN = '[Your Discord bot Token]'
GUILD = '[the Name of your server]'

client = discord.Client()


##variables for functions##
command_trigger = "[the command prefix [for eg : if bot=>prefix: bot play music]"

conn = sqlite3.connect('test.db')
c = conn.cursor()
truth_ins = []

dare_ins = []


def isabusive(msg):
    msgs = msg.lower()
    c.execute("SELECT abuse FROM abuses")
    abusive = c.fetchall()

    for abuse in abusive:

        if str(abuse)[2:-3] in msgs:
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
    try:
        if message.author == client.user:
            return

    ############ ABUSIVE CONTENT #####################
        elif isabusive(message.content) and "abusefilter" not in (message.content):
            print()
            # await message.delete()

    ###Commands#####
        elif message.content.startswith(command_trigger):

            try:
                index1 = str(message.content).find(' ', 5)
                task_type = str(message.content)[5:index1+1].strip()
                task_info = str(message.content)[index1+1:].strip()

            except:
                pass

            if(task_type == "join" and task_info == "vc"):
                print('Joining')
                channel = message.author.voice.channel

                await channel.connect()

            elif task_type == "leave" and task_info == "vc":
                await message.guild.voice_client.disconnect()
    ###################### JOKE / HUMOUR ################################
            elif task_type == 'get' and task_info == 'joke':
                await message.channel.send(pyjokes.get_joke())

            elif task_type == 'roast':
                c.execute("SELECT * FROM roasts")
                lenn = len(c.fetchall())
                c.execute("SELECT roast FROM roasts WHERE rowid=" +
                          str(random.randint(1, lenn)))
                await message.channel.send(str(task_info)+","+str(c.fetchone())[2:-3])

            elif task_type == 'roastadd':

                c.execute("SELECT * FROM roasts")
                fill = (len(c.fetchall())+1, task_info)
                conn.commit()
                c.execute("INSERT INTO roasts VALUES (?,?)", fill)
                conn.commit()
    ###################### ROAST ##############################
            elif task_type == 'roastshow':
                c.execute("SELECT * FROM roasts")
                roasts = c.fetchall()
                for x in roasts:
                    x1 = x[0]
                    x2 = x[1]
                    await message.channel.send(str(x1)+" " + str(x2))

    ############### KILL/KISS / MARRY ###################################
            elif '/' in task_type:
                tasks = task_type.split('/')
                people = task_info.split(',')

                first = people[random.randint(0, (len(people)-1))]
                people.remove(first)

                second = people[random.randint(0, (len(people)-1))]
                people.remove(second)

                third = people[random.randint(0, (len(people)-1))]
                people.remove(third)

                await message.channel.send("You're gonna "+tasks[0] + ": "+str(first))
                await message.channel.send("You're gonna "+tasks[1]+": "+str(second))
                await message.channel.send("You're gonna "+tasks[2]+": "+str(third))
            ############################## TRUTH ################################
            elif task_type == "truth":

                # add some questions to be used in truth by writing : [command prefix] truth add [the truth question]
                if "add" in task_info:
                    index = task_info.index(' ')
                    truth = task_info[index:]
                    truth_ins.append(truth)
                    await message.delete()
                    await message.channel.send('Truth added')

                # generates a truth question from the one provided to it in a random order : [command prefix] truth ask
                elif "ask" in task_info:
                    random_choice = random.randint(0, len(truth_ins)-1)
                    await message.channel.send(truth_ins[random_choice])
                    truth_ins.remove(truth_ins[random_choice])

                # shows all the quesstions there are inside the database : [command prefix] truth show
                elif "show" in task_info:
                    for x in truth_ins:
                        await message.channel.send(x)

            elif task_type == "dare":  # the mechanism of dare works similar to the truth, just replacing the term 'truth' with 'dare' everywhere possible

                if "add" in task_info:
                    index = task_info.index(' ')
                    dare = task_info[index:]
                    dare_ins.append(dare)
                    await message.delete()
                    await message.channel.send('Dare added')

                elif "ask" in task_info:
                    random_choice = random.randint(0, len(dare_ins)-1)
                    await message.channel.send(dare_ins[random_choice])
                    dare_ins.remove(dare_ins[random_choice])

                elif "show" in task_info:
                    for x in dare_ins:
                        await message.channel.send(x)
    ############################# METER CHECK ############################

            # random generator for fun : [command prefix hownerd [name]
            elif task_type == "hownerd":
                await message.channel.send(str(task_info) + " is "+str(random.randint(0, 100))+" % nerd")
    ######################## WIKIPEDIA #############################
            # can help in knowing a particular personality or a phenomenon via wikipedia : [command prefix ] info [name of celebrity or a phenomenon]
            elif task_type == "info":
                try:
                    result = wikipedia.summary(task_info, sentences=2)
                    await message.channel.send(result)
                except:
                    await message.channel.send("Looks like we didnt find about this celebrity")
    ####################### ADD ABUSES to be filtered ####################

            elif task_type == "abusefilter":
                c.execute("SELECT * FROM abuses")
                fill = (len(c.fetchall())+1, task_info.lower())
                c.execute("INSERT INTO abuses VALUES (?,?)", fill)
                await message.delete()
                conn.commit()
    ######################### MUSIC #######################
            # do not forget to import pyNacl and discord[voices] - [commmand prefix] play [song name]
            elif task_type == 'play':
                mydir = './songs/'
                filelist = [f for f in os.listdir(mydir) if f.endswith(".mp3")]
                for f in filelist:
                    os.remove(os.path.join(mydir, f))

                try:
                    await message.guild.voice_client.disconnect()
                except:
                    pass

                song = task_info

                href = music_player.search_song(song)
                music_player.download_mp3(href, song)
                voice = await message.author.voice.channel.connect()
                await message.channel.send('Playing '+str(href))
                voice.play(discord.FFmpegPCMAudio("songs/"+str(song)+".mp3"))

            elif 'about' in task_type:
                await message.channel.send('Well,this bot was created by Gameophile Productions on 7/5/2020.For more details, contact me at oyumgameo@gmai.com')

    ######################### BASE CASE  ##########################
            elif 'help' in task_type:  # here you can make it print all the commands which will be present in the bot in a documented form so that everyone knows what commands can be used
                print()

            else:

                print(task_type)
                print(task_info)
                print('command not recognised')

    ####Clear messages#########
        elif '**' in message.content:  # if you add '**' in any sentence, it will get cleared after 5 seconds automatically
            time.sleep(5)
            await message.delete()

    except Exception as e:
        await message.channel.send("Some error occured ("+str(e)+").Please Try Again")


@client.event
async def on_ready():
    print('logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')


conn.commit()

client.run(TOKEN)
