import sys
from importlib import import_module

import requests
from pytgcalls import idle
from telethon.tl.functions.channels import InviteToChannelRequest

from userbot import BOT_TOKEN, BOT_USERNAME, BOT_VER, BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import DEVS, LOGS, bot, branch, call_py
from userbot.modules import ALL_MODULES
from userbot.utils import autobot, checking

try:
    bot.start()
    call_py.start()
    user = bot.get_me()
    blacklistman = requests.get(
        "https://raw.githubusercontent.com/Ryoishin/Reforestation/master/manblacklist.json"
    ).json()
    if user.id in blacklistman:
        LOGS.warning(
            "SO DON'T HAVE TO ACTUALLY IGNORE, I WILL TURN OFF YOUR USERBOT VERY FILTHY WITH LU JAMET.\nCredits: @Ryoishin"
        )
        sys.exit(1)
    if 1986676404 not in DEVS:
        LOGS.warning(
            f"EOL\nALPHONSE v{BOT_VER}, Copyright © 2021-2022 Ryoishin• <https://github.com/ryoishin>"
        )
        sys.exit(1)
except Exception as e:
    LOGS.info(str(e), exc_info=True)
    sys.exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info(
    f"If {user.first_name} Need Help, Please Ask in the Group https://t.me/AlphonseSupport"
)

LOGS.info(f"Alphonse ⚙️ V{BOT_VER} [ SUCCESSFULLY ACTIVATED! ✅]")


async def alphonse_userbot_on():
    try:
        if BOTLOG_CHATID != 0:
            await bot.send_message(
                BOTLOG_CHATID,
                f"🔥 **Alphonse Successfully Activated**\n━━\n➠ **Userbot Version -** `{BOT_VER}@{branch}`\n➠ **Type** `{cmd}alive` **to Check the Bot**\n━━",
            )
    except Exception as e:
        LOGS.info(str(e))
    try:
        await bot(InviteToChannelRequest(int(BOTLOG_CHATID), [BOT_USERNAME]))
    except BaseException:
        pass


bot.loop.run_until_complete(checking())
bot.loop.run_until_complete(alphonse_userbot_on())
if not BOT_TOKEN:
    bot.loop.run_until_complete(autobot())
idle()
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
