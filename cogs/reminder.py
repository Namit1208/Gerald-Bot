import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime

scheduler = AsyncIOScheduler()
scheduler.start()

# Dictionary to store reminders: {user_id: {reminder_id: {time, date, message, job}}}
reminders = {}

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remind(self, ctx, time: str, date: str, *, message: str):
        """Set a reminder: !remind HH:MM DD/MM/YYYY Meeting"""
        try:
            reminder_time = datetime.datetime.strptime(f"{time} {date}", "%H:%M %d/%m/%Y")

            if reminder_time <= datetime.datetime.now():
                await ctx.send("❌ Meow! Time must be in the future, hooman!")
                return

            # Generate a unique reminder ID
            reminder_id = len(reminders.get(ctx.author.id, {})) + 1

            # Store the reminder
            if ctx.author.id not in reminders:
                reminders[ctx.author.id] = {}

            reminders[ctx.author.id][reminder_id] = {
                "time": time,
                "date": date,
                "message": message,
                "job": scheduler.add_job(
                    self.send_reminder,
                    "date",
                    run_date=reminder_time,
                    args=[ctx, reminder_id, message],
                ),
            }

            await ctx.send(f"✅ Meow! Reminder `{reminder_id}` set for {time} on {date}!")

        except ValueError:
            await ctx.send("🚨 Meow Error! Use format: `!remind HH:MM DD/MM/YYYY Message`!")

    async def send_reminder(self, ctx, reminder_id, message):
        """Send the reminder and remove it from the list."""
        await ctx.send(f"🚀 Meow! Reminder `{reminder_id}`: {message}! Time to save the world! 🌍")
        if ctx.author.id in reminders and reminder_id in reminders[ctx.author.id]:
            del reminders[ctx.author.id][reminder_id]

    @commands.command()
    async def delete_reminder(self, ctx, reminder_id: int):
        """Delete a reminder by its ID: !delete_reminder 1"""
        if ctx.author.id in reminders and reminder_id in reminders[ctx.author.id]:
            reminders[ctx.author.id][reminder_id]["job"].remove()  # Remove the scheduled job
            del reminders[ctx.author.id][reminder_id]  # Delete the reminder
            await ctx.send(f"🗑️ Meow! Reminder `{reminder_id}` has been deleted!")
        else:
            await ctx.send(f"❌ Meow! Reminder `{reminder_id}` not found, hooman!")

    @commands.command()
    async def modify_reminder(self, ctx, reminder_id: int, time: str, date: str, *, message: str):
        """Modify a reminder: !modify_reminder 1 HH:MM DD/MM/YYYY New Message"""
        try:
            reminder_time = datetime.datetime.strptime(f"{time} {date}", "%H:%M %d/%m/%Y")

            if reminder_time <= datetime.datetime.now():
                await ctx.send("❌ Meow! Time must be in the future, hooman!")
                return

            if ctx.author.id in reminders and reminder_id in reminders[ctx.author.id]:
                # Remove the old job
                reminders[ctx.author.id][reminder_id]["job"].remove()

                # Update the reminder
                reminders[ctx.author.id][reminder_id] = {
                    "time": time,
                    "date": date,
                    "message": message,
                    "job": scheduler.add_job(
                        self.send_reminder,
                        "date",
                        run_date=reminder_time,
                        args=[ctx, reminder_id, message],
                    ),
                }

                await ctx.send(f"✅ Meow! Reminder `{reminder_id}` updated for {time} on {date}!")
            else:
                await ctx.send(f"❌ Meow! Reminder `{reminder_id}` not found, hooman!")

        except ValueError:
            await ctx.send("🚨 Meow Error! Use format: `!modify_reminder ID HH:MM DD/MM/YYYY New Message`!")

    @commands.command()
    async def list_reminders(self, ctx):
        """List all your active reminders: !list_reminders"""
        if ctx.author.id in reminders and reminders[ctx.author.id]:
            reminder_list = "\n".join(
                f"`{reminder_id}`: {reminder['message']} at {reminder['time']} on {reminder['date']}"
                for reminder_id, reminder in reminders[ctx.author.id].items()
            )
            await ctx.send(f"📅 Meow! Your reminders:\n{reminder_list}")
        else:
            await ctx.send("❌ Meow! You have no active reminders, hooman!")

async def setup(bot):
    await bot.add_cog(Reminders(bot))