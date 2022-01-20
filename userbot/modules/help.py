""" Userbot help command """

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.help(?: |$)(.*)")
async def help(event):
    """For .help command,"""
    args = event.pattern_match.group(1).lower()
    # Prevent Channel Bug to get any information and command from all modules
    if event.is_channel and not event.is_group:
        await event.edit("`Help command isn't permitted on channels`")
        return
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Please specify a valid module name.")
    else:
        final = "**List of all loaded module(s)[🤖](https://telegra.ph/file/aaacd9d754a0a2b9c2522.jpg)**\n\
                 \nSpecify which module do you want help for! \
                 \n**Usage:** `.help` <module name>\n\n"
                  link_preview=True

        temp = "".join(str(i) + " " for i in CMD_HELP)
        temp = sorted(temp.split())
        for i in temp:
            final += "`" + str(i)
            final += "`\t\t\t☆\t\t\t "
        await event.edit(f"{final[:-5]}")
