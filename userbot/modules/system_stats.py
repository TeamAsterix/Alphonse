""" Userbot module for getting information about the server. """

import time
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from os import remove
from platform import python_version, uname
from shutil import which

from telethon import version
from telethon.errors.rpcerrorlist import MediaEmptyError

from userbot import (
    ALIVE_NAME,
    ALIVE_PIC,
    CMD_HELP,
    CUSTOM_ALIVE_EMOJI,
    CUSTOM_ALIVE_TEXT,
    MENTION,
    UBOT_VER,
    StartTime,
    bot,
    get_readable_time,
)
from userbot.events import register


@register(outgoing=True, pattern=r"^\.sysd$")
async def sysdetails(sysd):
    """For .sysd command, get system info using neofetch."""
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch",
                "--stdout",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("**Install neofetch first!**")


@register(outgoing=True, pattern=r"^\.botver$")
async def bot_ver(event):
    """For .botver command, get the bot version."""
    if event.text[0].isalpha() or event.text[0] in ("/", "#", "@", "!"):
        return
    if which("git") is not None:
        ver = await asyncrunapp(
            "git",
            "describe",
            "--all",
            "--long",
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        rev = await asyncrunapp(
            "git",
            "rev-list",
            "--all",
            "--count",
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        await event.edit(f"**Userbot:** `{verout}`\n" f"**Revision:** `{revout}`\n")
    else:
        await event.edit("**Shame that you don't have git!**")


@register(outgoing=True, pattern=r"^\.pip(?: |$)(.*)")
async def pipcheck(pip):
    """For .pip command, do a pip search."""
    if pip.text[0].isalpha() or pip.text[0] in ("/", "#", "@", "!"):
        return
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit("**Searching...**")
        pipc = await asyncrunapp(
            "pip3",
            "search",
            pipmodule,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit("**Output too large, sending as file...**")
                with open("output.txt", "w+") as file:
                    file.write(pipout)
                await pip.client.send_file(
                    pip.chat_id,
                    "output.txt",
                    reply_to=pip.id,
                )
                remove("output.txt")
                return
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`"
                f"{pipout}"
                "`"
            )
        else:
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`No result returned/False`"
            )
    else:
        await pip.edit("**Use .help pip to see an example.**")


@register(outgoing=True, pattern=r"^\.alive$")
async def amireallyalive(alive):
    """For .alive command, check if the bot is running."""
    img = ALIVE_PIC
    uptime = await get_readable_time((time.time() - StartTime))
    output = (
        f"{CUSTOM_ALIVE_TEXT}\n\n"
        f"{CUSTOM_ALIVE_EMOJI} `Usᴇʀ :` {DEFAULTUSER}\n"
        f"{CUSTOM_ALIVE_EMOJI} `Uᴘᴛɪᴍᴇ :` {uptime}\n"
        f"{CUSTOM_ALIVE_EMOJI} `Pʏᴛʜᴏɴ Vᴇʀsɪᴏɴ :` {python_version()}\n"
        f"{CUSTOM_ALIVE_EMOJI} `Usᴇʀʙᴏᴛ Vᴇʀsɪᴏɴ :` {UBOT_VER}\n"
        f"{CUSTOM_ALIVE_EMOJI} `Tᴇʟᴇᴛʜᴏɴ Vᴇʀsɪᴏɴ :` {version.__version__}\n"
        f"{CUSTOM_ALIVE_EMOJI} `Pʏᴘɪ Vᴇʀsɪᴏɴ :` 0.0.1\n"
        f"{CUSTOM_ALIVE_EMOJI} `Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ :` [Group](t.me/AlphonseSupport)\n"
    )
    if ALIVE_PIC:
        try:
            img = ALIVE_PIC
            pic_alive = await bot.send_file(alive.chat_id, img, caption=output)
            await alive.delete()
        except MediaEmptyError:
            await alive.edit(
                output + "\n\n *`The provided logo is invalid."
                "\nMake sure the link is directed to the logo picture`"
            )
    else:
        await alive.edit(output)


@register(outgoing=True, pattern=r"^\.aliveu")
async def amireallyaliveuser(username):
    """For .aliveu command, change the username in the .alive command."""
    message = username.text
    if message != ".aliveu" and message[7:8] == " ":
        newuser = message[8:]
        global DEFAULTUSER
        DEFAULTUSER = newuser
    await username.edit(f"**Successfully changed user to** `{newuser}`**!**")


@register(outgoing=True, pattern=r"^\.resetalive$")
async def amireallyalivereset(ureset):
    """For .resetalive command, reset the username in the .alive command."""
    global DEFAULTUSER
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("**Successfully reset user for alive!**")


CMD_HELP.update(
    {
        "sysd": ">`.sysd`" "\nUsage: Shows system information using neofetch.",
        "botver": ">`.botver`" "\nUsage: Shows the userbot version.",
        "pip": ">`.pip <module(s)>`" "\nUsage: Does a search of pip modules(s).",
        "alive": ">`.alive`"
        "\nUsage: Type .alive to see wether your bot is working or not."
        "\n\n>`.aliveu <text>`"
        "\nUsage: Changes the 'user' in alive to the text you want."
        "\n\n>`.resetalive`"
        "\nUsage: Resets the user to default.",
    }
)
