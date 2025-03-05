import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = discord.utils.get(member.guild.text_channels, name="general")
        if welcome_channel:
            await welcome_channel.send(f"🌟 Meow! Welcome {member.mention}! Gerald is here to save the world! 🚀")

async def setup(bot):
    await bot.add_cog(Welcome(bot))

