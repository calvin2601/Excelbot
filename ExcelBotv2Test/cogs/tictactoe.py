'''WIP tictactoe - abandoned 2022'''

import discord
from discord.ext import commands

class tictactoe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tictactoeboard(self,ctx):
        theBoard = {'top-L': 'x', 'top-M': 'x', 'top-R': 'x', 'mid-L': 'x', 'mid-M': 'x', 'mid-R': 'x', 'low-L': 'x',
                    'low-M': 'x', 'low-R': 'x'}
        await ctx.send(theBoard['top-L'] + '|' + theBoard['top-M'] + '|' + theBoard['top-R'])
        await ctx.send('-+-+-')
        await ctx.send(theBoard['mid-L'] + '|' + theBoard['mid-M'] + '|' + theBoard['mid-R'])
        await ctx.send('-+-+-')
        await ctx.send(theBoard['low-L'] + '|' + theBoard['low-M'] + '|' + theBoard['low-R'])










def setup(client):
    client.add_cog(tictactoe(client))