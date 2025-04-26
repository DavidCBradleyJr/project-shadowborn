import discord
from discord.ext import commands
import random
import asyncio

from database.users import user_exists, create_user
from utils.class_stats import CLASS_STATS
from utils.quiz import run_quiz

class StartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="start")
    async def start(self, ctx):
        if await user_exists(ctx.author.id):
            await ctx.send("🛡️ You have already begun your journey, Hunter.")
            return

        # Assign random Rank
        rank = random.choices(
            ["E", "D", "C", "B", "A", "S"],
            weights=[40, 30, 15, 10, 4, 1],  
            k=1
        )[0]

        # Ask Pick or Quiz
        await ctx.send(
            "✨ Do you want to **pick your class** manually or **take a personality quiz**?\n"
            "Type `pick` or `quiz`."
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("⏰ You took too long. Please run `/start` again.")
            return

        if msg.content.lower() == "pick":
            class_options = ", ".join(CLASS_STATS.keys())
            await ctx.send(f"🛡️ Available Classes: {class_options}\nType your class choice:")

            try:
                class_choice = await self.bot.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("⏰ You took too long. Please run `/start` again.")
                return

            chosen_class = class_choice.content.title()
            if chosen_class not in CLASS_STATS:
                await ctx.send("❌ Invalid class. Please run `/start` again.")
                return

        elif msg.content.lower() == "quiz":
            chosen_class = await run_quiz(ctx, self.bot)
        else:
            await ctx.send("❌ Invalid choice. Please type `pick` or `quiz`.")
            return

        # Pull base stats
        stats = CLASS_STATS[chosen_class]

        # Save to database
        await create_user(
            user_id=ctx.author.id,
            username=str(ctx.author),
            rank=rank,
            user_class=chosen_class,
            **stats
        )

        # Assign Discord Role
        guild = ctx.guild
        role_name = f"{chosen_class}"
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            role = await guild.create_role(name=role_name)
            print(f"[+] Created new role: {role_name}")
        await ctx.author.add_roles(role)
        await ctx.send(f"🛡️ You have been granted the **{role_name}** role.")

        # Send Welcome Embed
        embed = discord.Embed(title="🌌 Welcome to Project Shadowborn", color=discord.Color.purple())
        embed.add_field(name="Hunter", value=f"{ctx.author.display_name}", inline=True)
        embed.add_field(name="Rank", value=f"{rank}-Rank", inline=True)
        embed.add_field(name="Class", value=f"{chosen_class}", inline=True)

        embed.add_field(name="HP", value=stats['hp'])
        embed.add_field(name="Attack", value=stats['attack'])
        embed.add_field(name="Magic Attack", value=stats['magic_attack'])
        embed.add_field(name="Defense", value=stats['defense'])
        embed.add_field(name="Speed", value=stats['speed'])
        embed.add_field(name="Mana", value=stats['mana'])

        embed.set_footer(text="Your journey as a Hunter begins...")

        await ctx.send(embed=embed)
