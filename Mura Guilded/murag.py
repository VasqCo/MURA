#!/usr/bin/env python3
#IMPORT LIBRARIES
import guilded
import time
from pytube import YouTube, Playlist
import os, sys
from moviepy.editor import *
from dotenv import load_dotenv
load_dotenv('.env')

client = guilded.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')



@client.event
async def on_message(message):
    #Define important things
    msg = str(message.content)
    channel = message.channel
    user = message.author
    channel = str(channel).replace('Unknown User', f'{user}')
    msgformat = f'{username} - {channel} : {msg}'
    print(msgformat)

    if msg.lower().startswith('breadbomb '):
        command, mention = msg.split()
        #Checks if the author of the message is breadbombing themselves and sends a unique message if they are
        if mention == (message.author.mention):
            await channel.send('I-')
            await channel.typing()
            time.sleep(2)
            await channel.send('Ok')
            time.sleep(1)
        try:
            if mention != 'here'.lower():
                #Format mention for reading
                mention = mention.replace("<","")
                mention = mention.replace(">","")
                mention = mention.replace("@","")
                mention = mention.replace("!","")

                #Grab user from guilded
                user = await client.fetch_user(mention)

                username = str(user.name).split('#')[0]
                await channel.send(f'Sending breadbomb to {username}.')
                for i in range(50):
                    await user.send(':bread:')
                await channel.send(f'{username} has been breadbombed.')
            else:
                for i in range(50): #Unleash hell
                    await channel.send(':bread:')
        except guilded.errors.Forbidden:
            await channel.send('I cannot send messages to that user')
        except guilded.errors.HTTPException:
            await channel.send(':angry:')

    if 'women' in msg.lower() and message.author != client.user:
        await channel.send('women :coffee:')
    
    if msg.lower().startswith('say, '):
        command, say = msg.split(', ')
        await message.delete()
        await channel.send(say)
        

client.run(str(os.getenv('TOKEN')))
