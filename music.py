from asyncio.queues import Queue
import discord
import os
import asyncio
from discord import message
import youtube_dl
from discord.ext import commands
from discord.ext import tasks

from ytdl import YTDLSource

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.command()
    async def join(self, ctx):#*, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        print(f"{ctx.message}")

        channel: discord.VoiceChannel
        channel = ctx.message.author.voice.channel

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():

            if ctx.voice_client.is_playing():
                ...
                self.queue.append(url)
                await ctx.send(f'Queued {url}!')
            else:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                await ctx.send(f'Now playing: {player.title}')
                ctx.voice_client.play(player, after=lambda e: self.play_next(ctx, e))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        self.queue.clear()
        ctx.voice_client.stop()

        await ctx.voice_client.disconnect()

    # TODO: Store the title of the video that is to be played based on the supplied query in the "play" command
    @commands.command()
    async def queue(self, ctx):
        if len(self.queue) > 0:
            async with ctx.typing():
                titles = ''

                for (i, url) in enumerate(self.queue):
                    title = await YTDLSource.query_to_title(url, loop=self.bot.loop, stream=True)
                    titles += f'{i+1}. {title}\n'
                await ctx.send(f'{titles}')
        else:
            async with ctx.typing():
                await ctx.send(f'Queue is empty!')

    @commands.command()
    async def skip(self, ctx):
        """Skip to the next item in the queue or, if the queue is empty, stop playback"""
        ctx.voice_client.stop()

    def play_next(self, ctx, e):
        if e:
            print(f'Player error: {e}')
        if len(self.queue) >= 1:
            url = self.queue.pop(0)
            player = asyncio.run_coroutine_threadsafe(YTDLSource.from_url(url, loop=self.bot.loop, stream=True), self.bot.loop)
            ctx.voice_client.play(player.result(), after=lambda e: self.play_next(ctx, e))
        else:
            ...
            asyncio.run_coroutine_threadsafe(ctx.send('Queue finished...'), self.bot.loop)
            

    @play.before_invoke
    # @yt.before_invoke
    # @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ...
            # ctx.voice_client.stop()
