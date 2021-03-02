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

####### HOSTED ON REPL.it ########

############# IF you know how python works(database,env environment and sockets), you are free to check this out, you wont have much trouble....
############# If you are new to python , you can just clone this up , make up a bot in discord developer portal and add its token inside the TOKEN variable, and youre good to go!You can also add basic features inside once you learn some basics about this program


TOKEN ='your token'#YOUR Token Here
GUILD ='your guild name'

client = discord.Client()



bot = commands.Bot(command_prefix="$")
##variables for functions##
command_trigger="bot "

conn = sqlite3.connect('bot.db')
c=conn.cursor()
truth_ins=[]

dare_ins=[]

def isabusive(msg):
    msgs=msg.lower()
    c.execute("SELECT abuse FROM abuses")
    abusive=c.fetchall()

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
          await message.delete()
      
  ###Commands#####
      elif message.content.startswith(command_trigger):

        try:
          index1=str(message.content).find(' ',5)
          task_type=str(message.content)[5:index1+1].strip()
          task_info=str(message.content)[index1+1:].strip()

        except:
          pass

        if(task_type == "join" and task_info == "vc"):
          print('Joining')
          channel = message.author.voice.channel
      
          await channel.connect()
        
        elif task_type == "leave" and task_info == "vc":
          await message.guild.voice_client.disconnect()
  ###################### JOKE / HUMOUR ################################
        elif task_type=='get' and task_info == 'joke':
          await message.channel.send(pyjokes.get_joke())

        elif task_type=='roast':
          c.execute("SELECT * FROM roasts")
          lenn=len(c.fetchall())
          c.execute("SELECT roast FROM roasts WHERE rowid="+str(random.randint(1,lenn)))
          await message.channel.send(str(task_info)+","+str(c.fetchone())[2:-3])

        elif task_type=='roastadd':

          c.execute("SELECT * FROM roasts")
          fill=(len(c.fetchall())+1,task_info)
          conn.commit()
          c.execute("INSERT INTO roasts VALUES (?,?)",fill)
          conn.commit()
  ###################### ROAST ##############################
        elif task_type=='roastshow':
          c.execute("SELECT * FROM roasts")
          roasts=c.fetchall()
          for x in roasts:
            x1=x[0]
            x2=x[1]
            await message.channel.send(str(x1)+" "+ str(x2))

          
  ############### GAME ###################################                       Example: bot kill/punch/kiss name1,name2,name3 [output: You will kill (one among the persons) , you will punch [person] and you will kiss [person]
        elif '/' in task_type:
          tasks=task_type.split('/')
          people=task_info.split(',')
          
          first=people[random.randint(0,(len(people)-1))]
          people.remove(first)

          second=people[random.randint(0,(len(people)-1))]
          people.remove(second)

          third=people[random.randint(0,(len(people)-1))]
          people.remove(third)
          
          
          await message.channel.send("You're gonna "+tasks[0]+ ": "+str(first))
          await message.channel.send("You're gonna "+tasks[1]+": "+str(second))
          await message.channel.send("You're gonna "+tasks[2]+": "+str(third))
        ############################## TRUTH ################################
        elif task_type=="truth":                                                                #Truth and dare game

          if "add" in task_info:
            index=task_info.index(' ')                                                      #bot truth add [truth statement] (you can add your truth statements and can ask the bot to provide one out of them by using bot truth ask](same scenario for dare(just replace truth with dare)
            truth=task_info[index:]
            truth_ins.append(truth)
            await message.delete()
            await message.channel.send('Truth added')

          elif "ask" in task_info:
            random_choice = random.randint(0,len(truth_ins)-1)
            await message.channel.send(truth_ins[random_choice])
            truth_ins.remove(truth_ins[random_choice])

          elif "show" in task_info:
            for x in truth_ins:
              await message.channel.send(x)
        
        elif task_type=="dare":

          if "add" in task_info:
            index=task_info.index(' ')
            dare=task_info[index:]
            dare_ins.append(dare)
            await message.delete()
            await message.channel.send('Dare added')

          elif "ask" in task_info:
            random_choice=random.randint(0,len(dare_ins)-1)
            await message.channel.send(dare_ins[random_choice])
            dare_ins.remove(dare_ins[random_choice])

          elif "show" in task_info:
            for x in dare_ins:
              await message.channel.send(x)
  ############################# METER CHECK ############################            Sarcastic testmeter , you canchange values according to your creativity to make it more fun     
        elif task_type=="howinsane":
          await message.channel.send(str(task_info) +" is "+str(random.randint(0,100))+" % insane") #bot howinsane [person]
            
            
  ######################## WIKIPEDIA #############################      To get information regarding celebrities/Complex terms   
        elif task_type=="info":          #bot info [name of celebrity]
          try:
            result = wikipedia.summary(task_info, sentences = 2)
            await message.channel.send(result)
          except:
            await message.channel.send("Looks like we didnt find about this celebrity")
  ####################### ADD ABUSES ####################

        elif task_type=="abusefilter":                                  #to remove abusive content from server(you can add abusive contents inside a database{SQLite} insdie a table named abuses)
          c.execute("SELECT * FROM abuses")#abuses is the name of the table inside the database where all the words which need to be filtered are stored
          fill=(len(c.fetchall())+1,task_info.lower())
          c.execute("INSERT INTO abuses VALUES (?,?)",fill )
          await message.delete()
          conn.commit()
  ######################### MUSIC #######################
        elif task_type=='play':      #bot play [name of song]
          mydir='./songs/'
          filelist = [ f for f in os.listdir(mydir) if f.endswith(".mp3") ]
          for f in filelist:
            os.remove(os.path.join(mydir, f))

          try:
            await message.guild.voice_client.disconnect()
          except:
            pass

          song=task_info

          href=music_player.search_song(song)
          music_player.download_mp3(href,song)
          voice = await message.author.voice.channel.connect()
          await message.channel.send('Playing '+str(href))
          voice.play(discord.FFmpegPCMAudio("songs/"+str(song)+".mp3"))

        elif 'about' in task_type :
          await message.channel.send('Well,this bot was created by Gameophile Productions on 1/3/2021.For more details, contact me at oyumgameo@gmai.com')

  ######################### BASE CASE  ##########################
        elif 'help' in task_type:#I was feeling lazy to fill this up but this is the help section where anyone can get to know how the bot works....
          print()
        else:

          print(task_type)
          print(task_info)
          print('command not recognised')


  ####Clear messages#########
      elif '**' in message.content:           #Made this during the early phase as a test :P It just clears the message you write which include ** in them 
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
keep_alive.keep_alive()

client.run(TOKEN)



#now some of you might think why i didnt use Bot.command for this project, well becase i wanted to build something which had a major role of python, using all of discord's API s and features are boring, I preferred making my own !You are welcome to suggest me or add yourself some new features in this project
#For more info you can contact me on oyumgameo@gmail.com
