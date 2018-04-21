#Libraries being investigated

#Discord API
import discord
#ASync lib
import asyncio
#Google Translate API
from googletrans import Translator
import youtube_dl
#Includes json and urllib, used for sending requests to google images
from google_images_download import google_images_download

import shutil, os, glob #file IO
import urllib.request
import urllib.parse
import re


#Moved token to seperate file for security reasons
TOKEN='ERROR MISSING TOKEN, THIS SHOULDNT DISPLAY'#in case the token fails, we want a meaningful error
TOKEN = (open("token.txt","r").readline()).strip()


client = discord.Client()
global inChat
global player
globals()["inChat"]=None
globals()["player"]=None

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$wheezer'):
        msg = 'https://cdn.discordapp.com/attachments/361994220916965387/435840858332332073/carl.jpeg'.format(message)
        await client.send_message(message.channel, msg)


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #Test Image Posting
    if message.content.startswith('$wheezer'):
        #Carl Wheezer (jimmy neutron) image
        msg = 'https://cdn.discordapp.com/attachments/361994220916965387/435840858332332073/carl.jpeg'.format(message)
        await client.send_message(message.channel, msg)
        return


    #Translation
    elif message.content.startswith('$trans'):
        #List with every langauge code supported by google translate
        languages=['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'zh-CN', 'zh-TW', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'ny', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tl', 'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']

        #Output a basic menu asking the user for input
        await client.send_message(message.channel, 'Select a choice for translating: \n 1: From detected source language to English \n 2: From detected source language to provided destination langauge  \n 3: From provided source language to provided destination langauge args')
        selection=await client.wait_for_message(timeout=120,author=message.author, channel=message.channel)

        #Set defaults for translating
        translator =Translator()
        msg = 'An error occurred: Unknown Error, contact Zach'
        await client.send_message(message.channel, 'Enter your sentence')
        sentence=await client.wait_for_message(timeout=120,author=message.author, channel=message.channel)

        try:
            if (selection.content=='1' or selection.content=='$1'):
                result=translator.translate(sentence.content)
            elif(selection.content=='2' or selection.content=='$2'):
                await client.send_message(message.channel, 'Enter The langauge to translate to')
                destLang=await client.wait_for_message(timeout=120,author=message.author, channel=message.channel)
                result=translator.translate(sentence.content,destLang.content)
            elif(selection.content=='3' or selection.content=='$3'):
                await client.send_message(message.channel, 'Enter The langauge to translate to')
                destLang=await client.wait_for_message(timeout=120,author=message.author, channel=message.channel)
                await client.send_message(message.channel, 'Enter The langauge to translate from')
                sourceLang=await client.wait_for_message(timeout=120,author=message.author, channel=message.channel)
                result=translator.translate(sentence.content,destLang.content,sourceLang.content)
            else:
                await client.send_message(message.channel, 'An error occurred: Invalid Selection')
                return
        except:
            await client.send_message(message.channel, 'An error occurred: Invalid language(s)')
            return
        if(result):
            msg='Translated Text:  '+result.text
        await client.send_message(message.channel, msg)
        return


    #images
    elif(message.content.startswith('$image')):
        try:
            #split the message up into seperate terms for querying
            Keywords=message.content[7:]
            response = google_images_download.googleimagesdownload()
            #get an image with arguments and download it
            arguments = {"keywords":Keywords,"limit":1,"format":"jpg"}
            response.download(arguments)

            #upload the image to the server
            upDir=os.getcwd()+'/downloads/'+Keywords+"/"
            for root, dirs, files in os.walk(upDir):
                for file in files:
                    if (file.endswith('.jpg') or file.endswith('.jpeg')):
                        await client.send_file(message.channel, upDir+file)





            #Delete image after using
            delDir=os.getcwd()+'/downloads'
            shutil.rmtree(delDir)
            return


        except:
            await client.send_message(message.channel, 'An error occured:  Check your parameters')


    elif(message.content.startswith('$play')):
        terms=message.content[5:]
        searchTerms = urllib.parse.urlencode({"search_query" : terms})
        searchUrl = urllib.request.urlopen("http://www.youtube.com/results?" + searchTerms)
        searchResults = re.findall(r'href=\"\/watch\?v=(.{11})', searchUrl.read().decode())
        #We want the second video in the array as the first is almost always an ad
        videoUrl="http://www.youtube.com/watch?v="+searchResults[1]
        if(globals()["inChat"] is None):
            voice_channel = message.author.voice.voice_channel
            globals()["inChat"] = await client.join_voice_channel(voice_channel)
            #If the bot is already in the voice channel, add to queue
        else:
            await client.send_message(message.channel, 'Adding your song to queue')
        if(globals()["player"] is None):
            globals()["player"] = await inChat.create_ytdl_player(videoUrl)
            globals()["player"].start()
        return

    #Easter Eggs
    elif(message.content.startswith('$steamedhams')):
        videoUrl="https://www.youtube.com/watch?v=aRsOBFhNjVM"
        if(globals()["inChat"] is None):
            voice_channel = message.author.voice.voice_channel
            globals()["inChat"] = await client.join_voice_channel(voice_channel)
            #If the bot is already in the voice channel, add to queue
        else:
            await client.send_message(message.channel, 'Adding your song to queue')
        if(globals()["player"] is None):
            globals()["player"] = await inChat.create_ytdl_player(videoUrl)
            globals()["player"].start()
            await client.send_message(message.channel, 'https://i.ytimg.com/vi/ozXMsFZMydw/maxresdefault.jpg')
        return


    elif(message.content.startswith('$stop')):
        if(globals()["inChat"] is not None):
            globals()["player"].stop()
            await globals()["inChat"].disconnect()
            globals()["player"]=None
            globals()["inChat"]=None
        else:
            await client.send_message(message.channel, 'An error occured:  No song playing')
        return

    elif(message.content.startswith('$pause')):
        if(globals()["player"] is not None):
            player.pause()
        else:
            await client.send_message(message.channel, 'An error occured:  No song playing')
        return

    elif(message.content.startswith('$resume')):
        if(globals()["player"] is not None):
            player.resume()
        else:
            await client.send_message(message.channel, 'An error occured:  No song playing')
        return


    #help
    elif(message.content.startswith('$help')):
        subCommand=message.content.split(' ')
        #This list of commands is just to make sure everything is accounted for
        listOfCommands=['wheezer','help','image','play']
        if(len(subCommand)==1):
            await client.send_message(message.channel, 'Type $help [command] for command description\nList of commands:\nwheezer\ntrans\nimage\nplay')
            return
        elif(len(subCommand)==2):
            if(subCommand[1]=='wheezer'):
                await client.send_message(message.channel, 'Posts a picture of Carl Wheezer')
                return
            elif(subCommand[1]=='trans'):
                await client.send_message(message.channel, 'Translate text from on language to another')
                await client.send_message(message.channel, 'There are a couple options, you can specify the langauges translated or not')
                await client.send_message(message.channel, 'If specifying a langauge, you will need to use a Google language code')
                await client.send_message(message.channel, 'For a list of langauge codes and supported langauges, look here:  https://developers.google.com/admin-sdk/directory/v1/languages')
            elif(subCommand[1]=='image'):
                await client.send_message(message.channel, 'Pulls an image from Google Images')
                await client.send_message(message.channel, 'Usage:  $image [search terms]')
            elif(subCommand[1]=='play'):
                await client.send_message(message.channel, 'Plays a song from youtube')
                await client.send_message(message.channel, '\nUsage:  $play [search terms]\n$stop to end playlist\n$pause to pause playlist\n$skip to go to next song')
            else:
                await client.send_message(message.channel, subCommand[1])
                return
        else:
            await client.send_message(message.channel, 'An error occurred: too many arguments \nType $help to view a list of all commands or \nType $help [command] to get info on the specific command')
            return




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='$help'))


client.run(TOKEN)
