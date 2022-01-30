from datetime import datetime

from pytz import timezone
from telethon.events import ChatAction

from userbot import BLACKLIST_CHAT, BOTLOG_CHATID, CLEAN_WELCOME
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, LOGS, bot
from userbot.events import alphonse_cmd


@bot.on(ChatAction)
async def welcome_to_chat(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import (
            get_current_welcome_settings,
            update_previous_welcome,
        )
    except AttributeError:
        return
    cws = get_current_welcome_settings(event.chat_id)
if cws:
        """user_added=True,
        user_joined=True,
        user_left=False,
        user_kicked=False"""
        if (event.user_joined or event.user_added) and not (await event.get_user()).bot:
            if CLEAN_WELCOME:
                try:
await event.client.delete_messages(
                        event.chat_id, cws.previous_welcome
                    )
                except Exception as e:
                    LOGS.warn(str(e))
            a_user = await event.get_user()
chat = await event.get_chat()
            me = await event.client.get_me()

            # Current time in UTC
            now_utc = datetime.now(timezone("UTC"))

            # Convert to Jakarta time zone
            now_utc.astimezone(timezone("Asia/Jakarta"))
title = chat.title or "This Group"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
            first = a_user.first_name
            last = a_user.last_name
            fullname = f"{first} {last}" if last else first
            username = f"@{a_user.username}" if a_user.username else mention
            userid = a_user.id
my_first = me.first_name
            my_last = me.last_name
            my_fullname = f"{my_first} {my_last}" if my_last else my_first
            my_username = f"@{me.username}" if me.username else my_mention
            file_media = None
current_saved_welcome_message = None
            if cws:
                if cws.f_mesg_id:
                    msg_o = await event.client.get_messages(
                        entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
                    )
                    file_media = msg_o.media
current_saved_welcome_message = msg_o.message
                elif cws.reply:
                    current_saved_welcome_message = cws.reply
            current_message = await event.reply(
                current_saved_welcome_message.format(
                    mentions=mentions,
title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                ),
                file=file_media,
            )
update_previous_welcome(event.chat_id, current_message.id)


@bot.on(alphonse_cmd(outgoing=True, pattern=r"setwelcome(?: |$)(.*)"))
async def save_welcome(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await event.edit("**This command is prohibited in this group**")
try:
        from userbot.modules.sql_helper.welcome_sql import add_welcome_setting
    except AttributeError:
        return await event.edit("**Running In Non-SQL Mode!**")
    msg = await event.get_reply_message()
    string = event.pattern_match.group(1)
    msg_id = None
if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**#WELCOME \nGROUPID:** `{event.chat_id}`"
                "\nInstall the Welcome Group Command Message, This is a Welcome Message Record "
"Please Don't Delete!",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            return await event.edit(
"**To create media as Welcome message** `BOTLOG_CHATID` **Must be set.**"
            )
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "**Successfully Saved Welcome Message {} **"
if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        await event.edit(success.format("Here"))
    else:
        await event.edit(success.format("Here"))


@bot.on(alphonse_cmd(outgoing=True, pattern=r"checkwelcome$"))
async def show_welcome(event):
    try:
from userbot.modules.sql_helper.welcome_sql import get_current_welcome_settings
    except AttributeError:
        return await event.edit("`Running on Non-SQL mode!`")
    cws = get_current_welcome_settings(event.chat_id)
    if not cws:
return await event.edit("**No Welcome Message You Saved**")
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
        )
        await event.edit("**You have created a welcome message here**")
await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await event.edit("**You have created a welcome message here**")
        await event.reply(cws.reply)


@bot.on(alphonse_cmd(outgoing=True, pattern=r"rmwelcome$"))
async def del_welcome(event):
    try:
from userbot.modules.sql_helper.welcome_sql import rm_welcome_setting
    except AttributeError:
        return await event.edit("`Running on Non-SQL mode!`")
    if rm_welcome_setting(event.chat_id) is True:
        await event.edit("**Successfully Deleting Welcome Message Here**")
    else:
await event.edit("**No Welcome Message You Saved**")


CMD_HELP.update(
    {
        "welcome": f"**Plugin : **`welcome`\
        \n\n • **Syntax :** `{cmd}setwelcome` <welcome message> or reply to message type `.setwelcome`\
\n • **Function : **Save group welcome messages.\
        \n\n • **Syntax :** `{cmd}checkwelcome`\
        \n • **Function : **Check your saved welcome message.\
        \n\n • **Syntax :** `{cmd}rmwelcome`\
\n • **Function : **Delete your saved welcome message."
        "\n\n • **Variable Formats that can be used in setwelcome :**\
`{mention}`, `{title}`, `{count}`, `{first}`, `{last}`, `{fullname}`, `{userid}`, `{username}`, `{ my_first}`, `{my_fullname}`, `{my_last}`, `{my_mention}`, `{my_username}`\
    "
    }
)
