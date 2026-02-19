import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os
import asyncio
from discord import app_commands

# --- 1. WEB SERVER FOR RENDER/UPTIMEROBOT ---
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. BOT SETUP ---
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    # This syncs the slash commands to your server
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    print(f"Logged in as {bot.user.name}")

# --- 3. FONT TRANSFORMERS ---

def to_asian_style(text):
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙"
    )
    return text.translate(mapping)

def to_mixed(text):
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "ΔβĆĐ€₣ǤĦƗĴҜŁΜŇØƤΩŘŞŦỮVŴЖ¥ŽΔβĆĐ€₣ǤĦƗĴҜŁΜŇØƤΩŘŞŦỮVŴЖ¥Ž"
    )
    return text.translate(mapping)

def to_medieval(text):
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"
    )
    return text.translate(mapping)

def to_antique(text):
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"
    )
    return text.translate(mapping)

def to_monospace(text):
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"
    )
    return text.translate(mapping)

def to_circled(text):
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨"
    )
    return text.translate(mapping)

# --- 4. ROLE CONFIGURATION ---

ROLE_STYLES = {
    "OWNER": {"prefix": "👑 ", "transform": to_medieval},
    "MC PLAYER": {"transform": to_antique},
    "IRON": {"prefix": "🧲 ","transform": to_asian_style},
    "DIAMOND": {"prefix": "💎 ", "transform": to_circled},
    "NETHERITE": {"prefix": "🔥 ", "transform": to_monospace},
    "SUS": {"prefix": "ඞ ", "transform": None},
    "NOOB": {"prefix": "🦍 ", "transform": to_mixed},
    "COPPER": {"prefix": "🤎 ", "transform": None}
}

# --- 5. LOGIC ---
# --- HELPER FUNCTION ---
# This does the heavy lifting of checking roles and applying fonts
async def sync_member_nick(member):
    # Use Global Display Name as the "Reset" base, fallback to username
    base_name = member.global_name if member.global_name else member.name
    
    # Check roles from highest to lowest
    for role in reversed(member.roles):
        if role.name in ROLE_STYLES:
            style = ROLE_STYLES[role.name]
            
            # Apply font to the clean base name
            new_name = style["transform"](base_name) if style.get("transform") else base_name
            prefix = style.get("prefix", "")
            final_nick = f"{prefix}{new_name}"[:32]

            # Only edit if the nickname is actually different
            if member.nick != final_nick:
                try:
                    await member.edit(nick=final_nick)
                    print(f"Synced {member.name}'s nick to: {final_nick}")
                except discord.Forbidden:
                    print(f"Failed to rename {member.name}. Hierarchy issue!")
            return 

    # If no styled roles found, reset to default (None)
    if member.nick is not None:
        try:
            await member.edit(nick=None)
        except discord.Forbidden:
            pass






# --- HELPER: PROGRESS BAR ---
def make_progress_bar(current, total):
    size = 10
    filled = int((current / total) * size)
    bar = "🟩" * filled + "⬜" * (size - filled)
    percent = int((current / total) * 100)
    return f"[{bar}] {percent}% ({current}/{total})"

# --- 6. SLASH COMMANDS ---

@bot.tree.command(name="syncall", description="Safely update all member nicknames with a progress bar")
async def syncall(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Admin only!", ephemeral=True)

    await interaction.response.defer(ephemeral=False)
    
    # Get list of non-bot members
    members = [m for m in interaction.guild.members if not m.bot]
    total = len(members)
    
    if total == 0:
        return await interaction.followup.send("No members found to sync. Check your Intents!")

    message = await interaction.followup.send(f"🔄 **Starting Sync...**\n{make_progress_bar(0, total)}")
    
    count = 0
    for member in members:
        await sync_member_nick(member)
        count += 1
        
        # Update the progress bar every 5 members to avoid Discord rate limits
        if count % 5 == 0 or count == total:
            await message.edit(content=f"🔄 **Syncing Server...**\n{make_progress_bar(count, total)}")
        
        await asyncio.sleep(1.5) 

    await message.edit(content=f"✅ **Sync Complete!**\n{make_progress_bar(total, total)}\nUpdated {total} members.")

@bot.tree.command(name="clearall", description="Reset everyone to their original display names safely")
async def clearall(interaction: discord.Interaction):
    # 1. Permission Check
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Admin only!", ephemeral=True)

    # 2. Defer (Tells Discord to wait while we loop)
    await interaction.response.defer(ephemeral=False)
    
    # 3. Get members with nicknames
    members_with_nicks = [m for m in interaction.guild.members if m.nick is not None]
    total = len(members_with_nicks)

    if total == 0:
        return await interaction.followup.send("✅ Everyone already has their original name!")

    message = await interaction.followup.send(f"🧹 **Clearing Nicknames...**\n{make_progress_bar(0, total)}")
    
    count = 0
    for member in members_with_nicks:
        try:
            await member.edit(nick=None)
            count += 1
            
            # Update progress bar every 5 resets
            if count % 5 == 0 or count == total:
                await message.edit(content=f"🧹 **Clearing Nicknames...**\n{make_progress_bar(count, total)}")
            
            # Safety delay to avoid Discord rate limits
            await asyncio.sleep(1.5)
        except discord.Forbidden:
            continue
                
    await message.edit(content=f"✅ **Cleanup Complete!**\nRestored **{count}** members to their original names.")

# --- 7. THE FIX: RELIABLE SYNCING ---

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    try:
        # This force-syncs commands to the current server for instant results
        # Replace 'YOUR_SERVER_ID' with your actual server ID if it still doesn't show
        synced = await bot.tree.sync()
        print(f"Successfully synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# --- EVENTS ---

@bot.event
async def on_member_update(before, after):
    # Triggered when roles change or nicknames are manually changed
    if before.roles != after.roles:
        await sync_member_nick(after)

@bot.event
async def on_user_update(before, after):
    # Triggered when a user changes their Global Display Name or Avatar
    # Since 'after' here is a User object, we need to find them in your server
    for guild in bot.guilds:
        member = guild.get_member(after.id)
        if member:
            await sync_member_nick(member)


# --- 6. RUN ---
if __name__ == "__main__":
    keep_alive()
    # It will look for your token in Render's Environment Variables
    bot.run(os.environ.get('DISCORD_TOKEN'))
