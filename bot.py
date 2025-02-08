import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables (for securely storing the bot token in a .env file)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configure the bot with required intents
intents = discord.Intents.default()
intents.members = True  # For member-related events
intents.message_content = True  # For reading message content (commands, manual responses, etc.)

bot = commands.Bot(command_prefix="!", intents=intents)

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
# SETTINGS (Streamer's Discord User ID and Announcement Channel)
# --------------------------------------------------------------------
STREAMER_USER_ID = 163006577693949952  # Replace with actual streamer's Discord user ID

# --------------------------------------------------------------------
# 1. ON READY EVENT (Bot startup confirmation)
# --------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f"[DEBUG] Bot is online and connected as: {bot.user}")

# --------------------------------------------------------------------
# 2. GREETING NEW MEMBERS
# --------------------------------------------------------------------
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")  # Customize this channel name
    if channel:
        await channel.send(f"🎉 {member.mention}, welcome to the server! 🎮")

# --------------------------------------------------------------------
# 3. GOING LIVE NOTIFICATION
# --------------------------------------------------------------------
@bot.command()
async def goinglive(ctx, *, announcement: str = "@everyone I'm live now! Come watch: https://www.twitch.tv/example"):
    """
    Notify members that the streamer is live on a specific channel.
    """
    print(f"[DEBUG] Going live command invoked by: {ctx.author.name} (ID: {ctx.author.id})")

    if ctx.author.id != 163006577693949952:
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
# 4. SHOUT-OUT COMMAND
# --------------------------------------------------------------------
@bot.command()
async def shoutout(ctx, streamer: str = None):
    """Shoutsout selected user and their Twitch."""
    if streamer is None:
        await ctx.send("Please provide the streamer's name! Example: `!shoutout StreamerName`")
    else:
        await ctx.send(f"🎙️ Big shoutout to @{streamer}! https://www.twitch.tv/{streamer} Check them out and give them some love! 💖")

# --------------------------------------------------------------------
# 5. USEFUL RESOURCES COMMAND
# --------------------------------------------------------------------
@bot.command()
async def resources(ctx):
    """Shows all the best websites for BDO."""
    bdo_resources = """
📚 **Black Desert Online Resources**:
- [BDO Planner](https://bdoplanner.com/) - Gear and builds planner.
- [Garmoth.com](https://garmoth.com/) - Boss timers, node wars, horse breeds, and more.
- [Grumpy Green](https://grumpygreen.cricket/) - Life skilling and beginner guides.
- [BDO Codex](https://bdocodex.com/) - Item, quest, and NPC database.
Happy grinding, adventurer! 🎮
"""
    await ctx.send(bdo_resources)

# --------------------------------------------------------------------
# 6. GEAR UPGRADE PLANNER COMMAND
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
            await ctx.send("❌ Please provide exactly 6 gear enhancement levels!")
            return

        await ctx.send("Are you using **Kharazad** or **Distortion** earrings? Reply with `Kharazad` or `Distortion`.")
        msg = await bot.wait_for("message", check=check, timeout=60)
        earring_type = msg.content.lower()

        if earring_type not in ["kharazad", "distortion"]:
            await ctx.send("❌ Invalid earring type! Provide either `Kharazad` or `Distortion`.")
            return

        upgrade_plan = []
        for idx, level in enumerate(gear_levels):
            next_level = level + 1
            if next_level in ENHANCEMENT_DATA:
                upgrade_detail = ENHANCEMENT_DATA[next_level]
                upgrade_plan.append({
                    "gear": ACCESSORY_NAMES[idx],
                    "upgrade": upgrade_detail["level_name"],
                    "cron_cost": upgrade_detail["cron_cost"],
                    "base_rate": upgrade_detail["base_rate"],
                })

        upgrade_plan = sorted(upgrade_plan, key=lambda x: x["cron_cost"])
        response = "**Your next 3 cheapest upgrades:**\n"

        total_cost = 0
        for i, upgrade in enumerate(upgrade_plan[:3], start=1):
            cost = upgrade["cron_cost"] * 1000000
            total_cost += cost
            response += (
                f"**{i}. {upgrade['gear']}**:\n"
                f"- Upgrade: {upgrade['upgrade']}\n"
                f"- Cron Stone Cost: {cost:,} silver\n"
                f"- Base Success Rate: {upgrade['base_rate']}%\n"
            )
        response += f"\n**Total Estimated Cost: {total_cost:,} silver**"
        await ctx.send(response)

    except ValueError:
        await ctx.send("❌ Invalid input! Use numeric values like `0 2 1 3 4 5`.")
    except Exception as e:
        await ctx.send("❌ An error occurred. Please try again.")
        print(f"[ERROR] {e}")

# --------------------------------------------------------------------
# 7. COMMAND LIST (SHOW ALL BOT COMMANDS)
# --------------------------------------------------------------------
@bot.command()
async def commands(ctx):
    """List all available bot commands."""
    commands_list = "\n".join(
        [f"• **!{cmd.name}** - {cmd.help}" for cmd in bot.commands if not cmd.hidden]
    )
    await ctx.send(f"**Available Commands:**\n{commands_list}")

# --------------------------------------------------------------------
# 8. ERROR HANDLING
# --------------------------------------------------------------------
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You do not have permission to use this command.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❓ Command not found. Use `!commands` to see available commands.")
    else:
        await ctx.send("⚙️ An internal error occurred. Please try again later.")
        print(f"[ERROR] {error}")

# --------------------------------------------------------------------
# Start the bot
# --------------------------------------------------------------------
if TOKEN is None:
    print("[ERROR] Bot token is missing. Please check your .env file.")
else:
    bot.run(TOKEN)