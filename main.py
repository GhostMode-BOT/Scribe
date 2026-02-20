import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os
import asyncio
import json
from discord import app_commands

# --- 1. WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "I'm alive!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- 2. DATABASE LOGIC (JSON) ---
CONFIG_FILE = "role_config.json"

def load_styles():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            # We store function names as strings in JSON
            return json.load(f)
    return {}

def save_styles(styles):
    # Convert the dictionary to a format JSON can handle (removing the lambda objects)
    serializable = {}
    for role, data in styles.items():
        # Find the name of the font used
        font_name = "none"
        for name, func in FONT_MAP.items():
            if func == data["transform"]:
                font_name = name
        serializable[role] = {"prefix": data["prefix"], "font": font_name}
    
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=4)

# --- 3. BOT SETUP ---
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 4. FONT TRANSFORMERS ---
FONT_MAP = {
    "asian": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙")),
    "mixed": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "ΔβĆĐ€₣ǤĦƗĴҜŁΜŇØƤΩŘŞŦỮVŴЖ¥ŽΔβĆĐ€₣ǤĦƗĴҜŁΜŇØƤΩŘŞŦỮVŴЖ¥Ž")),
    "medieval": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟")),
    "antique": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃")),
    "monospace": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿")),
    "circled": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨")),
    "none": lambda t: t
}

# Initialize ROLE_STYLES from JSON
saved_data = load_styles()
ROLE_STYLES = {}
for role, data in saved_data.items():
    ROLE_STYLES[role] = {
        "prefix": data["prefix"],
        "transform": FONT_MAP.get(data["font"], FONT_MAP["none"])
    }

# --- 5. LOGIC HELPERS ---
async def sync_member_nick(member):
    base_name = member.global_name if member.global_name else member.name
    for role in reversed(member.roles):
        if role.name in ROLE_STYLES:
            style = ROLE_STYLES[role.name]
            new_name = style["transform"](base_name)
            prefix = style.get("prefix", "")
            final_nick = f"{prefix}{new_name}"[:32]
            if member.nick != final_nick:
                try: await member.edit(nick=final_nick)
                except discord.Forbidden: pass
            return 
    if member.nick is not None:
        try: await member.edit(nick=None)
        except discord.Forbidden: pass

def make_progress_bar(current, total):
    size = 10
    filled = int((current / total) * size)
    bar = "🟩" * filled + "⬜" * (size - filled)
    return f"[{bar}] {int((current/total)*100)}% ({current}/{total})"

# --- 6. SLASH COMMANDS ---

@bot.tree.command(name="createrole", description="Create a new role with specific permissions and color")
@app_commands.describe(
    name="Name of the role",
    level="Permission level: member, moderator, admin",
    hex_color="Hex color code (e.g. #ff0000 for red)"
)
async def createrole(interaction: discord.Interaction, name: str, level: str, hex_color: str = "#99aab5"):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Admin only!", ephemeral=True)

    # Convert Hex to Discord Color
    try:
        color_val = int(hex_color.replace("#", ""), 16)
        role_color = discord.Color(color_val)
    except ValueError:
        return await interaction.response.send_message("❌ Invalid Hex color! Use format #ffffff", ephemeral=True)

    # Permission Presets
    perms = discord.Permissions.none()
    if level.lower() == "member":
        perms.update(view_channel=True, send_messages=True, read_message_history=True, connect=True, speak=True)
    elif level.lower() == "moderator":
        perms.update(view_channel=True, send_messages=True, read_message_history=True, manage_messages=True, kick_members=True, ban_members=True, mute_members=True, move_members=True)
    elif level.lower() == "admin":
        perms.administrator = True
    else:
        return await interaction.response.send_message("❌ Invalid level! Choose: member, moderator, or admin", ephemeral=True)

    try:
        new_role = await interaction.guild.create_role(name=name, permissions=perms, color=role_color, reason=f"Created by {interaction.user}")
        await interaction.response.send_message(f"✅ Created role **{new_role.name}** with **{level}** permissions and color `{hex_color}`!")
    except discord.Forbidden:
        await interaction.response.send_message("❌ Bot lacks permission to create roles!")

@bot.tree.command(name="setrole", description="Configure or add a role's font style (Saved to Database)")
async def setrole(interaction: discord.Interaction, role_name: str, font_name: str, prefix: str = ""):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Admin only!", ephemeral=True)
    
    if font_name.lower() not in FONT_MAP:
        return await interaction.response.send_message(f"❌ Invalid font!", ephemeral=True)

    ROLE_STYLES[role_name] = {"prefix": prefix, "transform": FONT_MAP[font_name.lower()]}
    save_styles(ROLE_STYLES) # Save to JSON
    
    await interaction.response.send_message(f"✅ Role **{role_name}** configured and saved to database!")

@bot.tree.command(name="syncall", description="Safely update all member nicknames")
async def syncall(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator: return await interaction.response.send_message("❌ Admin only!", ephemeral=True)
    await interaction.response.defer(ephemeral=False)
    members = [m for m in interaction.guild.members if not m.bot]
    total = len(members)
    message = await interaction.followup.send(f"🔄 **Starting Sync...**\n{make_progress_bar(0, total)}")
    for i, member in enumerate(members, 1):
        await sync_member_nick(member)
        if i % 5 == 0 or i == total: await message.edit(content=f"🔄 **Syncing...**\n{make_progress_bar(i, total)}")
        await asyncio.sleep(1.5) 
    await message.edit(content=f"✅ **Sync Complete!**")

@bot.tree.command(name="clearall", description="Reset everyone to their original names")
async def clearall(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator: return await interaction.response.send_message("❌ Admin only!", ephemeral=True)
    await interaction.response.defer(ephemeral=False)
    members = [m for m in interaction.guild.members if m.nick is not None]
    total = len(members)
    if total == 0: return await interaction.followup.send("✅ Already clean!")
    message = await interaction.followup.send(f"🧹 **Clearing...**\n{make_progress_bar(0, total)}")
    for i, member in enumerate(members, 1):
        try: await member.edit(nick=None)
        except: pass
        if i % 5 == 0 or i == total: await message.edit(content=f"🧹 **Clearing...**\n{make_progress_bar(i, total)}")
        await asyncio.sleep(1.5)
    await message.edit(content=f"✅ **Cleanup Complete!**")

# --- 7. EVENTS ---
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"Synced slash commands. Database loaded with {len(ROLE_STYLES)} roles.")
    except Exception as e: print(e)

@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles: await sync_member_nick(after)

@bot.event
async def on_user_update(before, after):
    for guild in bot.guilds:
        member = guild.get_member(after.id)
        if member: await sync_member_nick(member)

if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ.get('DISCORD_TOKEN'))
