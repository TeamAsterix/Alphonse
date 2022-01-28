""" Userbot initialization. """

import logging
import os
import random
import re
import time
from datetime import datetime
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger
from math import ceil
from sys import version_info

from dotenv import load_dotenv
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from requests import get
from telethon import Button, events, functions, types
from telethon.sessions import StringSession
from telethon.sync import TelegramClient, custom, events
from telethon.utils import get_display_name

load_dotenv("config.env")

StartTime = time.time()

CMD_LIST = {}
# for later purposes
CMD_HELP = {}
INT_PLUG = ""
LOAD_PLUG = {}

# Bot Logs setup:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO
    )
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 8:
    LOGS.info(
        "You MUST have a python version of at least 3.8."
        "Multiple features depend on this. Bot quitting."
    )
    quit(1)

# Check if the config was edited by using the already used variable.
# Basically, its the 'virginity check' for the config file ;)
CONFIG_CHECK = os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________", None
)

if CONFIG_CHECK:
    LOGS.info(
        "Please remove the line mentioned in the first hashtag from the config.env file"
    )
    quit(1)

DEVS = (5095879452,)


# Check if the config was edited by using the already used variable.
# Basically, its the 'virginity check' for the config file ;)
CONFIG_CHECK = os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________"
)


# Telegram App KEY and HASH
API_KEY = int(os.environ.get("API_KEY", 0))
API_HASH = str(os.environ.get("API_HASH"))

# Userbot Session String
STRING_SESSION = os.environ.get("STRING_SESSION")

# Logging channel/group ID configuration.
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", 0))

# Userbot logging feature switch.
BOTLOG = str(os.environ.get("BOTLOG", "True"))
LOGSPAMMER = strtobool(os.environ.get("LOGSPAMMER", "True"))

# Bleep Blop, this is a bot ;)
PM_AUTO_BAN = strtobool(os.environ.get("PM_AUTO_BAN", "False"))

# Heroku Credentials for updater.
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")

# Sudo Users.
SUDO_USERS = os.environ.get("SUDO_USERS", None)

# Custom (forked) repo URL and BRANCH for updater.
UPSTREAM_REPO_URL = "https://github.com/TeamAlphonse/Alphonse"
UPSTREAM_REPO_BRANCH = "master"

# Console verbose logging
CONSOLE_LOGGER_VERBOSE = strtobool(os.environ.get("CONSOLE_LOGGER_VERBOSE") or "False")

# SQL Database URI
DB_URI = os.environ.get("DATABASE_URL")

# OCR API key
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY")

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY")

# Chrome Driver and Chrome Binaries
CHROME_DRIVER = "/usr/bin/chromedriver"
CHROME_BIN = "/usr/bin/chromium"

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID")
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY")

# Anti Spambot Config
ANTI_SPAMBOT = strtobool(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = strtobool(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# Default .alive name
ALIVE_NAME = "Master"

# Owner id to show profile link of given id as owner
OWNER_ID = os.environ.get("OWNER_ID", None)
if OWNER_ID:
    OWNER_ID = int(OWNER_ID)

# Default .alive pic
ALIVE_PIC = (
    os.environ.get("ALIVE_PIC") or "https://telegra.ph/file/9d264d95793ce0c15946b.jpg"
)

# For customizing there alive message
CUSTOM_ALIVE_TEXT = (
    os.environ.get("CUSTOM_ALIVE_TEXT") or "☆ Alphonse Is Running Perfect!"
)
CUSTOM_ALIVE_EMOJI = os.environ.get("CUSTOM_ALIVE_EMOJI") or "✮"

# Userbot version
UBOT_VER = "0.0.1"

# Time & Date - Country and Time Zone
COUNTRY = os.environ.get("COUNTRY")
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

# Zipfile module
ZIP_DOWNLOAD_DIRECTORY = os.environ.get("ZIP_DOWNLOAD_DIRECTORY") or "./zips"

# Clean Welcome
CLEAN_WELCOME = strtobool(os.environ.get("CLEAN_WELCOME") or "True")

# Last.fm Module
BIO_PREFIX = os.environ.get("BIO_PREFIX")
DEFAULT_BIO = os.environ.get("DEFAULT_BIO")

LASTFM_API = os.environ.get("LASTFM_API")
LASTFM_SECRET = os.environ.get("LASTFM_SECRET")
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME")
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD")
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)

lastfm = None
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    try:
        lastfm = LastFMNetwork(
            api_key=LASTFM_API,
            api_secret=LASTFM_SECRET,
            username=LASTFM_USERNAME,
            password_hash=LASTFM_PASS,
        )
    except Exception:
        pass

# Google Drive Module
G_DRIVE_DATA = os.environ.get("G_DRIVE_DATA")
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID")
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET")
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA")
G_DRIVE_FOLDER_ID = os.environ.get("G_DRIVE_FOLDER_ID")
G_DRIVE_INDEX_URL = os.environ.get("G_DRIVE_INDEX_URL")

TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./downloads/")

# Terminal Alias
TERM_ALIAS = os.environ.get("TERM_ALIAS")

# Deezloader
DEEZER_ARL_TOKEN = os.environ.get("DEEZER_ARL_TOKEN")

# Genius Lyrics API
GENIUS = os.environ.get("GENIUS_ACCESS_TOKEN")

# Uptobox
USR_TOKEN = os.environ.get("USR_TOKEN_UPTOBOX")

CMD_HANDLER = os.environ.get("CMD_HANDLER") or "."

SUDO_HANDLER = os.environ.get("SUDO_HANDLER", r"!")


def shutdown_bot(*_):
    LOGS.info("Received SIGTERM.")
    bot.disconnect()
    sys.exit(143)


signal.signal(signal.SIGTERM, shutdown_bot)


bot = TelegramClient(
    session=StringSession(STRING_SESSION),
    api_id=API_KEY,
    api_hash=API_HASH,
    connection=ConnectionTcpAbridged,
    auto_reconnect=True,
)


async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "You must set up the BOTLOG_CHATID variable in the config.env or environment variables, for the private error log storage to work."
        )
        sys.exit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "You must set up the BOTLOG_CHATID variable in the config.env or environment variables, for the userbot logging feature to work."
        )
        sys.exit(1)

    elif not (BOTLOG and LOGSPAMMER):
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Your account doesn't have rights to send messages to BOTLOG_CHATID "
            "group. Check if you typed the Chat ID correctly."
        )
        sys.exit(1)


with bot:
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGS.info(
            "BOTLOG_CHATID environment variable isn't a "
            "valid entity. Check your environment variables/config.env file."
        )
        sys.exit(1)


AKIRA_ID = ["1986676404"]
StartTime = time.time()
DEFAULTUSER = str(ALIVE_NAME)
USERID = str(OWNER_ID)
MENTION = f"[{DEFAULTUSER}](tg://user?id={USERID})"


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


async def update_restart_msg(chat_id, msg_id):
    img = ALIVE_PIC
    uptime = await get_readable_time((time.time() - StartTime))
    output = (
        f"{CUSTOM_ALIVE_TEXT}\n\n"
        f"{CUSTOM_ALIVE_EMOJI} `Usᴇʀ :` {MENTION}\n"
        f"{CUSTOM_ALIVE_EMOJI} `Uᴘᴛɪᴍᴇ :` {uptime}\n"
        f"{CUSTOM_ALIVE_EMOJI} `Pʏᴛʜᴏɴ Vᴇʀsɪᴏɴ :` {python_version()}\n"
        f"{CUSTOM_ALIVE_EMOJI} `Usᴇʀʙᴏᴛ Vᴇʀsɪᴏɴ :` {UBOT_VER}\n"
        f"{CUSTOM_ALIVE_EMOJI} `Tᴇʟᴇᴛʜᴏɴ Vᴇʀsɪᴏɴ :` {version.__version__}\n"
        f"{CUSTOM_ALIVE_EMOJI} `Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ :` [Group](t.me/AlphonseSupport)\n"
    )
    if ALIVE_PIC:
        try:
            img = ALIVE_PIC
            pic_alive = await bot.send_file(chat_id, msg_id, img, caption=output)
            await alive.delete()
        except MediaEmptyError:
            await alive.edit(
                output + "\n\n *`The provided logo is invalid."
                "\nMake sure the link is directed to the logo picture`"
            )
    else:
        await alive.edit(output)


try:
    from userbot.modules.sql_helper.globals import delgvar, gvarstatus

    chat_id, msg_id = gvarstatus("restartstatus").split("\n")
    with bot:
        try:
            bot.loop.run_until_complete(update_restart_msg(int(chat_id), int(msg_id)))
        except:
            pass
    delgvar("restartstatus")
except AttributeError:
    pass

# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None
SUDO_LIST = {}
CMD_LIST = {}
