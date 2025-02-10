import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure the bot with required intents
intents = discord.Intents.default()
intents.members = True  # For member-related events
intents.message_content = True  # For reading message content (commands, manual responses, etc.)

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# --------------------------------------------------------------------
# DATA (Enhancement levels and gear information)
# --------------------------------------------------------------------
ENHANCEMENT_DATA = {
    0: {"level_name": "+0 → PRI (I)", "base_rate": 16.3000, "additional_chance": 40, "cron_cost": 0, "agris_essence": 3},
    1: {"level_name": "PRI (I) → DUO (II)", "base_rate": 7.3000, "additional_chance": 60, "cron_cost": 120, "agris_essence": 5},
    2: {"level_name": "DUO (II) → TRI (III)", "base_rate": 4.5700, "additional_chance": 90, "cron_cost": 280, "agris_essence": 7},
    3: {"level_name": "TRI (III) → TET (IV)", "base_rate": 2.8900, "additional_chance": 130, "cron_cost": 540, "agris_essence": 8},
    4: {"level_name": "TET (IV) → PEN (V)", "base_rate": 1.9100, "additional_chance": 170, "cron_cost": 840, "agris_essence": 10},
    5: {"level_name": "PEN (V) → HEX (VI)", "base_rate": 1.2900, "additional_chance": 200, "cron_cost": 1090, "agris_essence": 12},
    6: {"level_name": "HEX (VI) → SEP (VII)", "base_rate": 0.8800, "additional_chance": 230, "cron_cost": 1480, "agris_essence": 15},
    7: {"level_name": "SEP (VII) → OCT (VIII)", "base_rate": 0.5700, "additional_chance": 260, "cron_cost": 1880, "agris_essence": 20},
    8: {"level_name": "OCT (VIII) → NOV (IX)", "base_rate": 0.3200, "additional_chance": 280, "cron_cost": 2850, "agris_essence": 25},
    9: {"level_name": "NOV (IX) → DEC (X)", "base_rate": 0.1720, "additional_chance": 300, "cron_cost": 3650, "agris_essence": 30},
}

ACCESSORY_NAMES = ["Necklace", "Belt", "Ring 1", "Ring 2", "Earring 1", "Earring 2"]

# --------------------------------------------------------------------
STREAMER_USER_ID = os.getenv("STREAMER_USER_ID")

# --------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f"[DEBUG] Bot is online and connected as: {bot.user}")

# --------------------------------------------------------------------
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")  # Customize this channel name
    if channel:
        await channel.send(f"🎉 {member.mention}, welcome to the server! 🎮")


# --------------------------------------------------------------------
@bot.command()
async def goinglive(ctx, announcement: str = None):
    """Announces that the user is going live."""
    if str(ctx.author.id) != STREAMER_USER_ID:
        await ctx.send("❌ You are not authorized to use this command.")
        print(f"[DEBUG] Unauthorized user attempted to use !goinglive: {ctx.author.name}")
        return

    channel = discord.utils.get(ctx.guild.text_channels, name="announcements")  # Customize this channel name
    if channel:
        await channel.send(f"🚨 {ctx.author.mention} is **LIVE**! {announcement}")
        print(f"[DEBUG] Sent live announcement to: {channel.name}")
    else:
        await ctx.send("❌ Announcements channel not found. Please create a channel named 'announcements'.")

# --------------------------------------------------------------------
@bot.command()
async def shoutout(ctx, streamer: str = None):
    """Shoutsout selected user and their Twitch."""
    if streamer is None:
        await ctx.send("Please provide the streamer's name! Example: `!shoutout StreamerName`")
    else:
        await ctx.send(f"🎙️ Big shoutout to @{streamer}! https://www.twitch.tv/{streamer} Check them out and give them some love! 💖")

# --------------------------------------------------------------------
@bot.command()
async def choicecommands(ctx):
    """Lists all available commands."""
    commands_list = """
    **Available Commands:**
    2. `!shoutout [streamer]` - Shouts out the selected user and their Twitch.
    3. `!resources` - Shows all the best websites for BDO.
    4. `!upgrade` - Calculate the next upgrades and associated costs for gear levels.
    """
    await ctx.send(commands_list)
# --------------------------------------------------------------------
@bot.command()
async def resources(ctx):
    """Shows all the best websites for BDO."""
    bdo_resources = """
📚 **Black Desert Online Resources**:
- [BDO Planner](https://bdoplanner.com/) - Gear and builds planner.
- [Garmoth.com](https://garmoth.com/) - Boss timers, market prices, and more.
- [BDO Nexus](https://bdo.altarofgaming.com/) - News, guides, and updates.
"""
    await ctx.send(bdo_resources)

# --------------------------------------------------------------------
@bot.command()
async def upgrade(ctx):
    """Calculate the next upgrades and associated costs for gear levels."""
    await ctx.send(
        "Please enter your gear enhancement levels in order, separated by spaces:\n"
        "Necklace Belt Ring 1 Ring 2 Earring 1 Earring 2\n"
        "Example: 1 2 2 0 3 3\n\n"
        "0 = +0, 1 = PRI, 2 = DUO, 3 = TRI, 4 = TET, 5 = PEN\n"
        "6 = HEX, 7 = SEP, 8 = OCT, 9 = NOV, 10 = DEC\n"
        "Note: You will be asked to clarify the earring type."
    )

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
        gear_levels = list(map(int, msg.content.split()))

        if len(gear_levels) != 6:
            await ctx.send("❌ Please provide exactly 6 gear levels.")
            return

        upgrade_info = []
        total_cron_cost = 0
        total_agris_essence = 0

        for i, level in enumerate(gear_levels):
            if level < 0 or level >= len(ENHANCEMENT_DATA):
                await ctx.send(f"❌ Invalid gear level: {level}. Please provide levels between 0 and {len(ENHANCEMENT_DATA) - 1}.")
                return

            next_level = level + 1
            if next_level < len(ENHANCEMENT_DATA):
                data = ENHANCEMENT_DATA[next_level]
                upgrade_info.append({
                    "accessory": ACCESSORY_NAMES[i],
                    "current_level": ENHANCEMENT_DATA[level]['level_name'],
                    "next_level": data['level_name'],
                    "base_rate": data['base_rate'],
                    "additional_chance": data['additional_chance'],
                    "cron_cost": data['cron_cost'],
                    "agris_essence": data['agris_essence'],
                    "total_cost": data['cron_cost'] + data['agris_essence']
                })
                total_cron_cost += data['cron_cost']
                total_agris_essence += data['agris_essence']

        # Sort upgrades by total cost (Cron Cost + Agris Essence)
        upgrade_info.sort(key=lambda x: x['total_cost'])

        # Get the top 3 cheapest upgrades
        cheapest_upgrades = upgrade_info[:3]

        # Calculate total silver and hours (assuming some conversion rates)
        total_silver = total_cron_cost * 1,000,000  # Example conversion rate
        total_hours = total_agris_essence * 0.5  # Example conversion rate

        upgrade_message = "\n".join([
            f"1. {upgrade['accessory']}: {upgrade['current_level']} → {upgrade['next_level']} "
            f"(Base Rate: {upgrade['base_rate']}%, "
            f"Cron Cost: {upgrade['cron_cost']}, Agris Essence: {upgrade['agris_essence']})"
            for upgrade in cheapest_upgrades
        ])
        upgrade_message += f"\n\nTotal Silver: {total_silver} silver\nTotal Hours: {total_hours} hours"

        await ctx.send(f"🔧 **Upgrade Information**:\n{upgrade_message}")

    except Exception as e:
        await ctx.send("❌ An error occurred while processing your request.")
        print(f"[ERROR] {e}")

# Run the bot with the token from the .env file
bot.run(os.getenv("DISCORD_TOKEN"))