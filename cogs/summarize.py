import discord
from discord.ext import commands

class Summarize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def summarize(self, ctx, *, text: str):
        """Summarizes long messages."""
        summary = text[:100] + "..." if len(text) > 100 else text
        await ctx.send(f"📜 Meow! Gerald summarized: {summary}")

async def setup(bot):
    await bot.add_cog(Summarize(bot))

