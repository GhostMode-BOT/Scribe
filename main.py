import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

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
