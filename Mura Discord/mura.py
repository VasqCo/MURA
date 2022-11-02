#!/usr/bin/env python3
#IMPORT LIBRARIES
import discord
from discord.ext import tasks
import time
from pytube import YouTube, Playlist
import os, sys
from moviepy.editor import *
from dotenv import load_dotenv
load_dotenv('.env')

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game('Hobo Horror 2'))



@client.event
async def on_message(message):
    #Define important things
    msg = str(message.content)
    channel = message.channel
    user = message.author
    username = str(message.author).split('#')[0]
    channel = str(channel).replace('Unknown User', f'{username}')
    msgformat = f'{username} - {channel} : {msg}'
    print(msgformat)

    #Download audio from youtube
    if msg.lower().startswith('download '):
        command, modifier, link = msg.split()
        # -v = single video
        if modifier == '-v':
            video = YouTube(link)
            await channel.send(f'Downloading {video.title}')
            download = video.streams.get_audio_only().download('download')
            audio = AudioFileClip(download)
            mp3 = download.split('.mp4')[0] + '.mp3'
            audio.write_audiofile(mp3)
            try:
                await channel.send(file=discord.File(mp3))
            except discord.errors.HTTPException:
                await channel.send('fil to big')
            os.remove(mp3)
            os.remove(download)
        # -p = list of videos
        if modifier == '-p':
            playlist = Playlist(link)
            await channel.send(f'Downloading {playlist.title}')
            for video in playlist.videos:
                await channel.send(f'Downloading {video.title}')
                download = video.streams.get_audio_only().download('/home/mcpi/Mura/download')
                audio = AudioFileClip(download)
                mp3 = download.split('.mp4')[0] + '.mp3'
                audio.write_audiofile(mp3, verbose=False)
                #Attempt to post the video but sends a message if it cannot
                try:
                    await channel.send(file=discord.File(mp3))
                except discord.errors.HTTPException:
                    await channel.send('The file is too large, moving on.')
                os.remove(mp3)
                os.remove(download)
                

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

                #Grab user from discord
                user = await client.fetch_user(mention)

                username = str(user.name).split('#')[0]
                await channel.send(f'Sending breadbomb to {username}.')
                for i in range(50):
                    await user.send(':bread:')
                await channel.send(f'{username} has been breadbombed.')
            else:
                for i in range(50): #Unleash hell
                    await channel.send(':bread:')
        except discord.errors.Forbidden:
            await channel.send('I cannot send messages to that user')
        except discord.errors.HTTPException:
            await channel.send(':angry:')

    if 'women' in msg.lower() and message.author != client.user:
        await channel.send('women :coffee:')
    
    if client.user.mentioned_in(message):
        await channel.send('stfu i\'m reading')
    
    if msg.lower().startswith('say, '):
        command, say = msg.split(', ')
        await message.delete()
        await channel.send(say)
        

client.run(os.getenv('TOKEN'))
