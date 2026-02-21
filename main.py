import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os
import asyncio
from discord import app_commands


# --- 1. WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "I'm alive!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- 2. BOT SETUP ---
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 3. FONT TRANSFORMERS ---
# We put these in a dictionary so the command can find them by name
FONT_MAP = {
    "asian": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙")),
    "mixed": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "ΔβĆĐ€₣ǤĦƗĴҜŁΜŇØƤΩŘŞŦỮVŴЖ¥ŽΔβĆĐ€₣ǤĦƗĴҜŁΜŇØƤΩŘŞŦỮVŴЖ¥Ž")),
    "medieval": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟")),
    "antique": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃")),
    "monospace": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿")),
    "circled": lambda t: t.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨")),
    "none": lambda t: t
}

# Your initial configuration
ROLE_STYLES = {
    "OWNER": {"prefix": "👑 ", "transform": FONT_MAP["medieval"]},
    "MC PLAYER": {"prefix": "🌏 ", "transform": FONT_MAP["antique"]},
    "IRON": {"prefix": "🧲 ","transform": FONT_MAP["asian"]},
    "DIAMOND": {"prefix": "💎 ", "transform": FONT_MAP["circled"]},
    "NETHERITE": {"prefix": "🔥 ", "transform": FONT_MAP["monospace"]},
    "SUS": {"prefix": "ඞ ", "transform": FONT_MAP["none"]},
    "NOOB": {"prefix": "☠️ ", "transform": FONT_MAP["mixed"]},
    "COPPER": {"prefix": "🤨 ", "transform": FONT_MAP["none"]}
}

# --- 4. HELPERS ---
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

# --- 5. SLASH COMMANDS ---

@bot.tree.command(name="setrole", description="Configure or add a role's font style")
@app_commands.describe(role_name="The EXACT name of the role", font_name="asian, mixed, medieval, antique, monospace, circled, none", prefix="Emoji or text to put before name")
async def setrole(interaction: discord.Interaction, role_name: str, font_name: str, prefix: str = ""):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Admin only!", ephemeral=True)
    
    if font_name.lower() not in FONT_MAP:
        return await interaction.response.send_message(f"❌ Invalid font! Choose: {', '.join(FONT_MAP.keys())}", ephemeral=True)

    ROLE_STYLES[role_name] = {
        "prefix": prefix,
        "transform": FONT_MAP[font_name.lower()]
    }
    
    await interaction.response.send_message(f"✅ Role **{role_name}** is now set to **{font_name}** style with prefix `{prefix}`.\n*Note: Use /syncall to apply this to existing members.*")

@bot.tree.command(name="listroles", description="See which font is assigned to which role")
async def listroles(interaction: discord.Interaction):
    if not ROLE_STYLES:
        return await interaction.response.send_message("No roles are currently configured.")
    
    output = "📜 **Current Role Configurations:**\n"
    for role, config in ROLE_STYLES.items():
        # Find font name by checking which function is in transform
        f_name = "custom"
        for name, func in FONT_MAP.items():
            if func == config["transform"]:
                f_name = name
        output += f"• **{role}**: Font: `{f_name}`, Prefix: `{config.get('prefix', 'None')}`\n"
    
    await interaction.response.send_message(output)

@bot.tree.command(name="syncall", description="Safely update all member nicknames")
async def syncall(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Admin only!", ephemeral=True)
    await interaction.response.defer(ephemeral=False)
    members = [m for m in interaction.guild.members if not m.bot]
    total = len(members)
    message = await interaction.followup.send(f"🔄 **Starting Sync...**\n{make_progress_bar(0, total)}")
    for i, member in enumerate(members, 1):
        await sync_member_nick(member)
        if i % 5 == 0 or i == total:
            await message.edit(content=f"🔄 **Syncing Server...**\n{make_progress_bar(i, total)}")
        await asyncio.sleep(1.5) 
    await message.edit(content=f"✅ **Sync Complete!**\nUpdated {total} members.")

@bot.tree.command(name="clearall", description="Reset everyone to their original names")
async def clearall(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Admin only!", ephemeral=True)
    await interaction.response.defer(ephemeral=False)
    members = [m for m in interaction.guild.members if m.nick is not None]
    total = len(members)
    if total == 0: return await interaction.followup.send("✅ Everyone is already clean!")
    message = await interaction.followup.send(f"🧹 **Clearing Nicknames...**\n{make_progress_bar(0, total)}")
    for i, member in enumerate(members, 1):
        try: await member.edit(nick=None)
        except: pass
        if i % 5 == 0 or i == total:
            await message.edit(content=f"🧹 **Clearing Nicknames...**\n{make_progress_bar(i, total)}")
        await asyncio.sleep(1.5)
    await message.edit(content=f"✅ **Cleanup Complete!**")

# --- 6. EVENTS ---
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"Synced slash commands. Logged in as {bot.user.name}")
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
