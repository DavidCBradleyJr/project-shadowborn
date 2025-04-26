import discord
from discord.ext import commands
import asyncio
import os

from dotenv import load_dotenv
from database.connection import init_db

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"[✅] Logged in as {bot.user}")
    await init_db()

async def load_cogs():
    from cogs.start import StartCog
    from cogs.profile import ProfileCog

    await bot.add_cog(StartCog(bot))
    await bot.add_cog(ProfileCog(bot))

if __name__ == "__main__":
    asyncio.run(load_cogs())
    bot.run(TOKEN)
