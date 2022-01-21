""" Userbot start point """

import sys,os
from importlib import import_module

from telethon.errors.rpcerrorlist import PhoneNumberInvalidError

from userbot import LOGS, bot
from userbot.modules import ALL_MODULES

INVALID_PH = (
    "\nError: Invalid phone number."
    "\nTip: Prefix number with country code"
    "\nor check your phone number and try again."
)

try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    sys.exit(1)


for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)


async def set_id():

    os.environ["OWNER_ID"] = (await bot.get_me()).id


LOGS.info("Your userbot is running!")

LOGS.info(
    "Congratulations, the bot is up and running! Send .help in any chat for more info.\n"
)

bot.loop.run_until_complete(set_id())
bot.run_until_disconnected()
