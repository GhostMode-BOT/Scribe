from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import os

# --- WEBSERVER FOR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- YOUR BOT CODE ---
# (Paste all your font transformers and role config here)

# At the bottom, before bot.run:

intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

# --- CUSTOM FONT TRANSFORMERS ---

def to_asian_style(text):
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙"
    )
    return text.translate(mapping)

def to_medieval(text):
    # For Owner
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"
    )
    return text.translate(mapping)

def to_antique(text):
    # Antique style for MC Player
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"
    )
    return text.translate(mapping)

def to_monospace(text):
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜ᴛ𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"
    )
    return text.translate(mapping)

def to_circled(text):
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨"
    )
    return text.translate(mapping)

# --- ROLE CONFIGURATION ---

ROLE_STYLES = {
    "OWNER": {"prefix": "👑 ", "transform": to_medieval},
    "MC PLAYER": {"transform": to_antique}, # Now Antique
    "IRON": {"transform": to_asian_style},
    "DIAMOND": {"prefix": "💎 ", "transform": to_circled},
    "NETHERITE": {"prefix": "🔥 ", "transform": to_monospace},
    "SUS": {"prefix": "ඞ ", "transform": None},
    "NOOB": {"prefix": " [L] ", "transform": None},
    "COPPER": {"prefix": "🤎 ", "transform": None}
}

@bot.event
async def on_member_update(before, after):
    # Fire only on role change
    if before.roles != after.roles:
        # Check from highest role to lowest
        for role in reversed(after.roles):
            if role.name in ROLE_STYLES:
                style = ROLE_STYLES[role.name]
                base_name = after.display_name
                
                # Transform font
                new_nick = style["transform"](base_name) if style.get("transform") else base_name
                prefix = style.get("prefix", "")
                final_nick = f"{prefix}{new_nick}"[:32]

                # Update nickname
                if after.nick != final_nick:
                    try:
                        await after.edit(nick=final_nick)
                        print(f"Applied {role.name} style to {after.name}")
                    except discord.Forbidden:
                        print(f"Forbidden: Cannot rename {after.name}. Check role hierarchy.")
                break



keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))