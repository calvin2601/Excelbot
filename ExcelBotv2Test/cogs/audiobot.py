import discord
from discord.ext import commands
import youtube_dl
import os
from discord.utils import get

class Audiobot(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def join(self,ctx):
        channel = ctx.message.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

    @commands.command()
    async def leave(self,ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self,ctx, *, query):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        source.volume = 0.05
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                os.remove(file)
        ydl_options ={'format':'bestaudio/best',
                     'postprocessors': [{'key': 'FFmpegExtractAudio',
                                         'preferredcodec': 'mp3',
                                         'preferredquality':'192'}]
}
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            ydl.download([url])

        for file in os.listdir('./'):
           if file.endswith('.mp3'):
               name = file
               break


        ctx.voice_client.play(discord.FFmpegPCMAudio(name))

    # #other option to join from 'HowToDoThings' video
    # @commands.command()
    # async def join2(self,ctx):
    #     channel = ctx.message.author.voice.channel
    #     voice = get(self.client.voice_clients, guild=ctx.guild)
    #
    #     if voice and voice.is_connected():
    #         await voice.move_to(channel)
    #     else:
    #         voice = await channel.connect()
    #
    #     await voice.disconnect()
    #
    #     if voice and voice.is_connected():
    #         await voice.move_to(channel)
    #     else:
    #         voice = await channel.connect()
    #         print(f"The bot has connected to {channel}\n")
    #
    #     await ctx.send(f"Joined {channel}")








def setup(client):
    client.add_cog(Audiobot(client))