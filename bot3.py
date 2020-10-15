import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import youtube_dl
from youtube_search import YoutubeSearch

bot = commands.Bot(command_prefix = '/')

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to discord...\n")

song_list = []

@bot.command(aliases=['seri'])
async def join(ctx):
    global song_list
    song_list = []
    try:
        await ctx.message.author.voice.channel.connect()
    except:
        await ctx.send('chal jhuti, VC to join karo')

@bot.command(aliases=['jbl','p'])
async def play(ctx,*args):

    global song_list

    if ctx.message.author.voice!=None and bot.voice_clients!=[]:

        song = ' '.join(args)
        song_list.append(song)

        if ctx.message.guild.voice_client.is_playing()==True:
            await ctx.send(f'**`{song}` ko line me dal diya**')
            return
        else:
            download(ctx.message.guild.voice_client)

def playsong(voice_client):

    try:
        song = song_list.pop(0)
    except:
        return

    results = YoutubeSearch(song,max_results=1).to_dict()
    for I in results:
        url = 'https://www.youtube.com' + I['url_suffix']

        ytdl_format_options = {
            'format' : 'bestaudio/best' ,
            'postprocessors' : [{
                'key' : 'FFmpegExtractAudio' ,
                'preferredcodec' : 'mp3' ,
                'preferredquality' : '320' ,
             }]
        }

        ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
        audio = ytdl.extract_info(I['link'],download = False)
        streamable_url = audio['formats'][0]['url']
        before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        voice_client.play(discord.FFmpegPCMAudio(streamable_url,before_options = before_options),after =lambda e: download(voice_client))

@bot.command(aliases=['line','q'])
async def queue(ctx):
    global song_list
    if song_list == []:
        await ctx.send('line me toh kuch nahi hai to kya gayega')
        return
    
    for i,s in enumerate(song_list):
        await ctx.send(f'*{i+1})*: **`{s}`**')
        

@bot.command(aliases = ['nikal','r'])
async def remove(ctx,position : int):
    global song_list
    if song_list == []:
        await ctx.send('line me toh kuch nahi hai to kya gayega')
        return

    try :
        await ctx.send(f'kya yaar, `{song_list[position-1]}` humse hi hatwana tha') 
        song_list.pop(position-1)
    except:
        await ctx.send('ek minute... ye kya, tumhara to number hi line ke bahar he')

@bot.command(aliases = ['rok'])
async def pause(ctx):
    if ctx.messgae.author.voice == None:
        await ctx.send('chal jhuti, VC to join karo')
        return
    ctx.message.guild.voice.client.pause()
    await ctx.send('Kyunnnnn gaana band kiya')

@bot.command(aliases = [])
async def resume(ctx):
    if ctx.messgae.author.voice == None:
        await ctx.send('chal jhuti, VC to join karo')
        return
    ctx.message.guild.voice_client.resume()
    await ctx.send('chalo naacho bache')

@bot.command(aliases = [])
async def skip(ctx):
    if ctx.messgae.author.voice == None:
        await ctx.send('chal jhuti, VC to join karo')
        return
    ctx.message.guild.voice_client.stop()
    await ctx.send('kya yaar, itna badhiya gane ko bajana ka ek mauka karab kiay')

@bot.command(aliases = [])
async def disconnect(ctx):
    global song_list
    for x in bot.voice_clients:
        if(x.guild == ctx.message.guild):
           song_list = []
           return await x.disconnect()
        if bot.voice_client==[]:
            await ctx.send('challo meh nikalta hoon')
              




bot.run('NzQ2Mjc2MzgwODUzMTQxNTE0.Xz9-Cg.kREhXuPwq2sTjXVT8Rcv_R3UWLY')

