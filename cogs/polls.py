import discord
from discord.ext import commands

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, question: str, *options):
        """Create a poll: !poll Question Option1 Option2"""
        if len(options) < 2:
            await ctx.send("Meow? A poll needs at least two options!")
            return
        
        poll_message = f"📊 **{question}**\n"
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        for i, option in enumerate(options[:10]):
            poll_message += f"{emojis[i]} {option}\n"
        
        msg = await ctx.send(poll_message)
        
        for i in range(len(options[:10])):
            await msg.add_reaction(emojis[i])

async def setup(bot):
    await bot.add_cog(Polls(bot))

