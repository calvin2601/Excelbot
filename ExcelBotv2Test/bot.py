import pandas as pd
import discord
import os
import asyncio
import praw
from datetime import datetime
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='\\')
bot_token = open('bottoken.txt','r').read()

ID = 'HgvyMVzkuCKOZg'
secret = 'xPGYVSnOfhX7n6VrZvq3uJg-V5I'
user_agent = 'discord:com.example.excelbot:v0.1 (by /u/calvin2601)'

reddit = praw.Reddit(client_id=ID,
                     client_secret=secret,
                     user_agent=user_agent)

@client.event
async def on_ready():
    reddit_deals.start()
    print('Bot is ready')

@tasks.loop(seconds= 60)
async def reddit_deals():

    #r/buildapcsales
    subreddit = reddit.subreddit('buildapcsalesuk')
    f = open('bapuks_ts.txt','r')
    timestamp = float(f.read())
    f.close()
    #print(timestamp)
    try:
        for submission in subreddit.new(limit=1):
            #print('In for loop')
            #print(submission.title)
            if submission.created_utc > timestamp:
                time = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                title = submission.title
                permalink = 'https://www.reddit.com' + submission.permalink
                channelID = 647839162229063680
                channel = client.get_channel(channelID)
                await channel.send(f'**{time}** \n{title} \n{permalink}')
                timestamp = submission.created_utc
                f = open('bapuks_ts.txt','w')
                f.write(str(timestamp))
                f.close()
    except:
        pass

    await asyncio.sleep(5)

    #r/nswdeals
    subreddit = reddit.subreddit('nintendoswitchdeals')
    f = open('nswdealsuk_ts.txt', 'r')
    timestamp = float(f.read())
    f.close()
    try:
        for submission in subreddit.search('uk', sort='new'):
            if submission.created_utc > timestamp:
                time = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                permalink = 'https://www.reddit.com' + submission.permalink
                title = submission.title
                channelID = 681855453222797334
                channel = client.get_channel(channelID)
                await channel.send(f'**{time}** \n{title} \n{permalink}')
                timestamp = submission.created_utc
                f = open('nswdealsuk_ts.txt', 'w')
                f.write(str(timestamp))
                f.close()
    except:
        pass

@client.command()
async def reload(ctx,extension):
    client.reload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} has been reloaded')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print(filename)
        client.load_extension(f'cogs.{filename[:-3]}')

# @client.command()
# async def mike(ctx):
#     await ctx.send('Mike is a sweaty nerd - Dom 2019')

client.run(bot_token)