import discord
from discord.ext import commands
from database.users import fetch_user_profile

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="profile")
    async def profile(self, ctx):
        user_data = await fetch_user_profile(ctx.author.id)
        if not user_data:
            await ctx.send("❌ You don't have a profile yet. Use `/start` to create your Hunter.")
            return

        embed = discord.Embed(
            title=f"🌌 {ctx.author.display_name}'s Hunter Profile",
            color=discord.Color.blue()
        )

        embed.add_field(name="Rank", value=f"{user_data['rank']}-Rank", inline=True)
        embed.add_field(name="Class", value=user_data['class'], inline=True)
        embed.add_field(name="Level", value=user_data['level'], inline=True)
        embed.add_field(name="EXP", value=f"{user_data['exp']} / {user_data['exp_to_next_level']}", inline=True)

        embed.add_field(name="HP", value=user_data['hp'])
        embed.add_field(name="Attack", value=user_data['attack'])
        embed.add_field(name="Magic Attack", value=user_data['magic_attack'])
        embed.add_field(name="Defense", value=user_data['defense'])
        embed.add_field(name="Speed", value=user_data['speed'])
        embed.add_field(name="Mana", value=user_data['mana'])

        embed.add_field(name="Gold", value=user_data['gold'], inline=True)
        embed.set_footer(text="Keep growing stronger, Hunter...")

        await ctx.send(embed=embed)
