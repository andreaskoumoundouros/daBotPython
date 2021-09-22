import discord
import os
import asyncio
from discord import message
import youtube_dl
from discord.ext import commands

import discord_token
from discord_token import MyToken
from music import Music

M_TOKEN = MyToken.get_token()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

bot = commands.Bot(command_prefix=commands.when_mentioned_or(":)"), description='Relatively simple music bot example')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

bot.add_cog(Music(bot))
bot.run(M_TOKEN)
