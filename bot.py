import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                if cog_name in bot.extensions:
                    await bot.unload_extension(cog_name)  # ✅ Unload first
                await bot.load_extension(cog_name)  # ✅ Load fresh
                print(f"✅ Loaded {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start("MTM0NjU3NjI1ODU5NDY0MDAwMw.G9NmWx.xMUANd7MSWw00h2FX1C_kGuJyCdJVdH5xtFoMo")

asyncio.run(main())
