import discord
from discord.ext import commands
import re

# Set up bot permissions so it can read text messages
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.command()
async def rate(ctx, *, pasted_text):
    """
    Type !rate and paste the entire NFL Universe stat block right next to it.
    """
    # Looks through the text for names, yards, touchdowns, and interceptions
    player_data = re.findall(r"Player:\s*([a-zA-Z0-9_]+).*?Yards:\s*(\d+).*?TDs:\s*(\d+).*?INTs:\s*(\d+)", pasted_text, re.IGNORECASE)
    
    if not player_data:
        await ctx.send("❌ **Error:** No stats found. Check your text format!")
        return

    response = "📊 **Scrim Performance Ratings (Out of 100)** 📊\n"
    response += "----------------------------------------------\n"

    for name, yards_str, tds_str, ints_str in player_data:
        yards, tds, ints = int(yards_str), int(tds_str), int(ints_str)
        
        # The math formula: Base 50 + yards + TDs - INTs
        base_score = 50
        score = base_score + (yards * 0.1) + (tds * 12) - (ints * 15)
        final_rating = max(0, min(100, round(score))) # Keeps it strictly between 0 and 100
        
        # Emojis based on how well they played
        emoji = "🔥" if final_rating >= 90 else "⭐" if final_rating >= 75 else "💪"
        response += f"{emoji} **{name}**: {final_rating}/100\n"

    await ctx.send(response)

# PASTE YOUR SECRET TOKEN INSIDE THE QUOTES BELOW:
import os
bot.run(os.getenv("DISCORD_TOKEN"))

