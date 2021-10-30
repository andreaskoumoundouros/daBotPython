import discord
import os
import asyncio
from discord import message
import youtube_dl
from discord.ext import commands

import discord_token
from discord_token import MyToken
from music import Music

import marcus_bot
from marcus_bot import Marcus
from generator import Generator

M_TOKEN = MyToken.get_token()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        else:
            print(message.author)

        if message.content == 'ping':
            await message.channel.send('pong')

bot = commands.Bot(command_prefix=commands.when_mentioned_or(":)"), description='Relatively simple music bot example')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

marcus = Marcus()

@bot.event
async def on_message(message):

    if message.author.id == 141637885718822913 and len(message.content) > 5:
        output = message.content
        net_out = marcus.get_output(output)
        await message.channel.send(net_out)
        print(f'sending: {net_out} in {message.channel}')

    await bot.process_commands(message)

bot.add_cog(Music(bot))
bot.add_cog(Generator(bot, marcus))
bot.run(M_TOKEN)
