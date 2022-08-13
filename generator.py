import random
import discord
import os
import asyncio
from discord import message
from discord.ext import commands
import json
from urllib import parse, request
from utilities import get_gif_url

class Generator(commands.Cog):
    def __init__(self, bot, marcus, malcs):
        self.bot = bot
        self.marcus = marcus
        self.malcs = malcs

    @commands.command()
    async def marcus_generate(self, ctx):

        output = ctx.message.content
        net_out = self.marcus.get_output(output)
        await ctx.message.channel.send(net_out)
        print(f'sending: {net_out} in {ctx.message.channel}')

    @commands.command()
    async def malcs_generate(self, ctx):

        output = ctx.message.content
        net_out = self.malcs.get_output(output)
        ctx.message.content = net_out

        chance = random.choice([x for x in range(0, 100)])
        if chance > 95:
            await ctx.message.channel.send(net_out)
            await self.send_gif(ctx)
        else:
            await ctx.message.channel.send(net_out)
            print(f'sending: {net_out} in {ctx.message.channel}')

    @commands.command()
    async def gif(self, ctx):
        await self.send_gif(ctx)

    async def send_gif(self, ctx):
        await ctx.message.channel.send(get_gif_url(ctx.message.content))