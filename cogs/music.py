import discord
from discord.ext import commands
import yt_dlp
from discord import FFmpegPCMAudio
from collections import deque

voice_client = None
song_queue = deque()

class GeraldBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def play_next(self, ctx):
        global voice_client, song_queue
        if song_queue:
            next_song = song_queue.popleft()
            source = FFmpegPCMAudio(next_song['url'])
            voice_client.play(source, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
            await ctx.send(f"🎶 Now playing: `{next_song['title']}`")
        else:
            await ctx.send("No more songs in the queue!")

    @commands.command()
    async def play(self, ctx, *, query: str):
        """Plays music from SoundCloud or adds to queue."""
        global voice_client, song_queue

        if not ctx.author.voice:
            await ctx.send("Meow! You need to be in a voice channel, hooman!")
            return
        
        channel = ctx.author.voice.channel

        if not voice_client or not voice_client.is_connected():
            voice_client = await channel.connect()

        await ctx.send(f"🎵 Searching for `{query}` on SoundCloud...")

        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1', 
        }

        def extract_info():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(query, download=False)

        info = await self.bot.loop.run_in_executor(None, extract_info)
        url2 = info['entries'][0]['url'] if 'entries' in info else info['url']
        song_info = {'title': info['title'], 'url': url2}

        if voice_client.is_playing():
            song_queue.append(song_info)
            await ctx.send(f"🎶 Added to queue: `{info['title']}`")
        else:
            song_queue.append(song_info)
            await self.play_next(ctx)

    @commands.command()
    async def stop(self, ctx):
        """Stops the music and disconnects."""
        global voice_client, song_queue
        if voice_client and voice_client.is_connected():
            song_queue.clear()
            await voice_client.disconnect()
            voice_client = None
            await ctx.send("Meow! Gerald has stopped the music and left the voice channel.")
        else:
            await ctx.send("Meow? Gerald is not even playing anything, hooman!")

    @commands.command()
    async def skip(self, ctx):
        """Skips the current song."""
        global voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("⏭️ Skipped the current song.")
        else:
            await ctx.send("Meow? There's nothing playing to skip, hooman!")

    @commands.command()
    async def queue(self, ctx):
        """Displays the current song queue."""
        if song_queue:
            queue_list = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(song_queue)])
            await ctx.send(f"🎶 Current queue:\n{queue_list}")
        else:
            await ctx.send("The queue is empty!")

    @commands.command()
    async def remove(self, ctx, index: int):
        """Removes a song from the queue by its index."""
        if 0 < index <= len(song_queue):
            removed_song = song_queue[index-1]
            song_queue.remove(removed_song)
            await ctx.send(f"Removed `{removed_song['title']}` from the queue.")
        else:
            await ctx.send("Invalid index, hooman!")

    @commands.command()
    async def commands_list(self, ctx):
        """Lists all available commands."""
        command_text = (
            "🐾 **GeraldBot Commands** 🐾\n"
            "`!remind HH:MM DD/MM/YYYY Message` - Sets a reminder.\n"
            "`!poll Question Option1 Option2 ...` - Creates a poll.\n"
            "`!chat Message` - Gerald responds with a fun message.\n"
            "`!play Song Name` - Plays music from SoundCloud.\n"
            "`!stop` - Stops music and disconnects.\n"
            "`!skip` - Skips the current song.\n"
            "`!queue` - Shows the current song queue.\n"
            "`!remove Index` - Removes a song from the queue by its index.\n"
            "`!commands_list` - Shows this command list."
        )
        await ctx.send(command_text)

async def setup(bot):
    await bot.add_cog(GeraldBot(bot))