import discord
from discord.ext import commands
import google.generativeai as genai
import asyncio

# Configure Gemini API
genai.configure(api_key="Given in Text box")

class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')  

    @commands.command(name="chat")
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def chat(self, ctx, *, message: str):
        """Generates a response using the Gemini AI model"""
        
        thinking_msg = await ctx.send("Thinking... 🤔")
        
        try:
            
            response = self.model.generate_content(message)
            
            
            reply = response.text if response.text else "Meow? I don't understand."
            
            
            await thinking_msg.delete()
            
            
            await ctx.send(reply)
        except Exception as e:
           
            await thinking_msg.delete()
            
            
            await ctx.send("Oops! Something went wrong. 😿")
            print(f"Error: {e}")
    @chat.error
    async def chat_error(self, ctx, error):
        """Handles errors for the chat command"""
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Slow down! You can use this command again in {error.retry_after:.2f} seconds.")

async def setup(bot):
    await bot.add_cog(ChatCog(bot))
