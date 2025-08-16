import discord
from discord.ext import commands

class Quote(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def mike(self,ctx):
        await ctx.send('Mike is a sweaty nerd - Dom 2019')
    @commands.command()
    async def vinny(self,ctx):
        await ctx.send('F*ck Vinny - Dom 2019')
    @commands.command()
    async def shotgun(self,ctx):
        await ctx.send('Shotguns are sh*t - Tom 2019 AKA Tom is sh*t at Destiny 2')
    @commands.command()
    async def jackie(self,ctx):
        await ctx.send('Jackie eats f*cking ribs on Burger Day 2016')
    @commands.command()
    async def dom(self,ctx):
        await ctx.send('Okay, boomer')
def setup(client):
    client.add_cog(Quote(client))