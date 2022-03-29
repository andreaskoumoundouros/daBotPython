import discord
import os
import asyncio
from discord import message
from discord.ext import commands


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
        await ctx.message.channel.send(net_out)
        print(f'sending: {net_out} in {ctx.message.channel}')
