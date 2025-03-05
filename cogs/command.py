import discord
from discord.ext import commands

class CommandList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="show_commands") 
    async def show_commands(self, ctx):
        """Lists all available commands."""
        command_text = (
            "🐾 **GeraldBot Commands** 🐾\n"
            "🎵 **Music Commands** 🎵\n"
            "`!play YouTube_URL or Song Name` - Plays music from YouTube or adds it to the queue.\n"
            "`!stop` - Stops music and disconnects.\n"
            "`!skip` - Skips the current song.\n"
            "`!queue` - Displays the current song queue.\n"
            "`!remove Index` - Removes a song from the queue by its index.\n"
            "\n"
            "⏰ **Reminder Commands** ⏰\n"
            "`!remind HH:MM DD/MM/YYYY Message` - Sets a reminder.\n"
            "`!delete_reminder ID` - Deletes a reminder by its ID.\n"
            "`!modify_reminder ID HH:MM DD/MM/YYYY New Message` - Modifies an existing reminder.\n"
            "`!list_reminders` - Lists all your active reminders.\n"
            "\n"
            "🎉 **Other Commands** 🎉\n"
            "`!poll Question Option1 Option2 ...` - Creates a poll.\n"
            "`!chat Message` - Gerald responds with a fun message.\n"
            "`!about` - Learn more about Gerald.\n"
            "`!show_commands` - Shows this command list.\n"
        )
        await ctx.send(command_text)

    @commands.command(name="about")
    async def about(self, ctx):
        """Displays information about Gerald."""
        about_text = (
            "Hi, I'm Gerald, the saviour of this world! 🌍\n"
            "I got these superpowers from my Master, **Namit Chugh**. 🦸‍♂️\n"
            "Just ask me anything! I may come for your help!!!! 🚀\n"
        )
        await ctx.send(about_text)

async def setup(bot):
    await bot.add_cog(CommandList(bot))