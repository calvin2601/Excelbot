import discord
from discord.ext import commands
from cogs.destinymodules import d2weaponsprocessingv2, d2armorprocessing, d2masterupdatelightgg, asynclightgg
import requests
import os
from bs4 import BeautifulSoup
import io
import aiohttp
import pandas as pd

class Destiny2(commands.Cog):
    def __init__(self, client):
        self.client = client

    def right_channel(self,ctx):
        listofchannels = [642132987152039977, 650706158432288779, 666421423887089677, 642705288834580511]
        return ctx.channel.id in listofchannels

    @commands.command()
    async def master(self,ctx):
        '''Sends the channel the masterfile containing the recommended perks for weapons from lightgg'''
        await ctx.send(file=discord.File('Master.csv'))

    @commands.command()
    async def updatemaster(self,ctx):
        '''Updates the masterfile containing the recommended perks for weapons from lightgg
        WARNING: WILL TAKE A LONG TIME'''

        await self.client.change_presence(activity=discord.Game(name='Scraping from light.gg'))
        await ctx.send('The bot is updating the masterlist and may go offline at some point. If the bot is not online after 45 mins of this message, let me know')

        #d2masterupdatelightgg.masterlistupdate()

        df = await asynclightgg.main()

        df.to_csv('masterv3.csv',index=False)

        await self.client.change_presence()

    @commands.command()
    async def weapons(self, ctx):
        '''Compares your inventory of weapons to the weapons on the masterlist. Get your inventory from DIM.
        Will only take .csv file'''
        if ctx.message.attachments[0].filename.endswith('csv'):
            await ctx.send('Attachment is recognised')

            #saving file to server

            url = ctx.message.attachments[0].url
            filename = str(ctx.message.author) + str(ctx.message.attachments[0].filename)
            r = requests.get(url)
            with open(filename,'wb') as f:
                f.write(r.content)
            await ctx.channel.purge(limit=1)
            await ctx.send('Download complete')
            # inventory1, master1 = d2weaponsprocessing.processfiles(filename)
            # inventorychecked = d2weaponsprocessing.comparison(master1,inventory1)
            inventorychecked = d2weaponsprocessingv2.processfiles(filename)
            inventorychecked.to_csv(filename,index=False)
            await ctx.channel.purge(limit=1)
            await ctx.send('Process complete')

            with open(filename,'rb') as fp:
                await ctx.send(file=discord.File(fp,filename))




    @commands.command()
    async def armour(self,ctx):
        '''Will calculate the sum of 3 stats. Must  include 3 of Int,Mob,Res,Rec,Dis,Str
        Can have multiple sets of 3
        Example: \armour Int,Mob,Res Rec,Dis,Int'''

        if ctx.message.attachments[0].filename.endswith('csv'):
            await ctx.send('Attachment is recognised')

            url = ctx.message.attachments[0].url
            filename = str(ctx.message.author) + str(ctx.message.attachments[0].filename)
            r = requests.get(url)

            with open(filename,'wb') as f:
                f.write(r.content)
            await ctx.channel.purge(limit=1)
            await ctx.send('Download complete')

            split = ctx.message.content.split(' ')
            split.pop(0)

            data=d2armorprocessing.armor(filename, split)

            data.to_csv(filename,index=False)
            await ctx.channel.purge(limit=1)
            await ctx.send('Process complete')

            with open(filename, 'rb') as fp:
                await ctx.send(file=discord.File(fp,filename))


    @commands.command()
    async def createexoticfile(self,ctx):
        print(ctx.author)
        f = open(f'{ctx.author}_exotic.txt','w')
        f.close()

    @commands.command()
    async def updateexotic(self,ctx,*,new_item):
        with open(f'{ctx.author}_exotic.txt','a') as f:
            f.write(f'\n{new_item}')

    @commands.command()
    async def xur(self,ctx):
        response = requests.get('https://ftw.in/game/destiny-2/find-xur')
        page_html_soup = BeautifulSoup(response.text,'html.parser')
        a = [entry.text for entry in page_html_soup.find_all('p') if 'located' in entry.text][0]
        await ctx.send(a)
        image_url = page_html_soup.find('a',rel='nofollow').get('href')
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'cool_image.png'))

        inventory = page_html_soup.find_all('ul')[-1].find_all('p')
        inventory_list = [entry.text for entry in inventory]
        item_dictionary = {}
        item_list = [entry.split(' [')[0].lower() for entry in inventory_list]
        for i in item_list:
            if i not in item_dictionary.keys():
                item_dictionary[i] = ''


        viable_users=[]
        for file in os.listdir('./'):
            if file.endswith('_exotic.txt'):
                viable_users.append(file.split('_')[0])

        for user in viable_users:
            with open(f'{user}_exotic.txt','r') as f:
                item_counter = 0
                for line in f:
                    print(line)
                    if line.lower().strip() in item_list:
                        item_dictionary[line.lower().strip()] += f' {user},'
                        item_counter+=1
                    if item_counter == 4:
                        break


        string = ''
        for i in inventory_list:
            string += '**' + i + '**' +'\n' + item_dictionary[i.split(' [')[0].lower()] + '\n\n'
        await ctx.send(string)

    @commands.command()
    async def gambitprimeroles(self,ctx):
        await ctx.send(file = discord.File('gambitprimeroles.png'))






def setup(client):
    client.add_cog(Destiny2(client))