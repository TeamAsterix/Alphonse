# Copyright (C) 2020 TeamUltroid
 # Ported by X_ImFine
 # Recode by @ryoishin

 import asyncio
 from datetime import datetime

 from telethon import events
 from telethon.tl import functions, types

 from userbot import BOTLOG_CHATID
 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP, bot, owner
 from userbot.events import alphonse_cmd
 from userbot.utils import bash

 USER_AFK = {}
 afk_time = None
 last_afk_message = {}
 last_afk_msg = {}
 afk_start = {}


 @bot.on(events.NewMessage(outgoing=True))
 @bot.on(events.MessageEdited(outgoing=True))
 async def set_not_afk(event):
     global USER_AFK
     global afk_time
     global last_afk_message
     global afk_start
     global afk_end
     back_alive = datetime.now()
     afk_end = back_alive.replace(microsecond=0)
     if afk_start != {}:
         total_afk_time = str((afk_end - afk_start))
     current_message = event.message.message
     if "afk" not in current_message and "yes" in USER_AFK:
         try:
             if pic.endswith((".tgs", ".webp")):
                 shite = await event.client.send_message(event.chat_id, file=pic)
                 shites = await event.client.send_message(
                     event.chat_id,
                     f"**{owner} Back Online For Parming**\n**From AFK :** `{total_afk_time}` **Last**",
                 )
             else:
                 shite = await event.client.send_message(
                     event.chat_id,
                     f"**{owner} Unemployment pretentious Busy Back Again!**\n**From AFK :** `{total_afk_time}` **Last**",
                     file=pic,
                 )
         except BaseException:
             shite = await event.client.send_message(
                 event.chat_id,
                 f"**{owner} Back Online**\n**From AFK :** `{total_afk_time}` **Last**",
             )

         await asyncio.sleep(6)
         await shite.delete()
         try:
             await shites.delete()
         except BaseException:
             pass
         USER_AFK = {}
         afk_time = None

         await bash("rm -rf *.webp")
         await bash("rm -rf *.mp4")
         await bash("rm -rf *.tgs")
         await bash("rm -rf *.png")
         await bash("rm -rf *.jpg")


 @bot.on(
     events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private))
 )
 async def on_afk(event):
     if event.fwd_from:
         return
     global USER_AFK
     global afk_time
     global last_afk_message
     global afk_start
     global afk_end
     back_alivee = datetime.now()
     afk_end = back_alivee.replace(microsecond=0)
     if afk_start != {}:
         total_afk_time = str((afk_end - afk_start))
     current_message_text = event.message.message.lower()
     if "afk" in current_message_text:
         return False
     if USER_AFK and not (await event.get_sender()).bot:
         msg = None
         if reason:
             message_to_reply = (
                 f"**✘ {owner} On AFK** `{total_afk_time}` **Last **\n"
                 + f"**✦҈͜͡➳ Because :** `{reason}`"
             )
         else:
             message_to_reply = (
                 f"**✘ Sorry {owner} Currently AFK** `{total_afk_time}` **Last **"
             )
         try:
             if pic.endswith((".tgs", ".webp")):
                 msg = await event.reply(file=pic)
                 msgs = await event.reply(message_to_reply)
             else:
                 msg = await event.reply(message_to_reply, file=pic)
         except BaseException:
             msg = await event.reply(message_to_reply)
         await asyncio.sleep(2.5)
         if event.chat_id in last_afk_message:
             await last_afk_message[event.chat_id].delete()
         try:
             if event.chat_id in last_afk_msg:
                 await last_afk_msg[event.chat_id].delete()
         except BaseException:
             pass
         last_afk_message[event.chat_id] = msg
         try:
             if msgs:
                 last_afk_msg[event.chat_id] = msgs
         except BaseException:
             pass


 @bot.on(alphonse_cmd(outgoing=True, pattern="afk(?: |$)(.*)"))
 async def _(event):
     if event.fwd_from:
         return
     reply = await event.get_reply_message()
     global USER_AFK
     global afk_time
     global last_afk_message
     global last_afk_msg
     global afk_start
     global afk_end
     global reason
     global pic
     USER_AFK = {}
     afk_time = None
     last_afk_message = {}
     last_afk_msg = {}
     afk_end = {}
     start_1 = datetime.now()
     afk_start = start_1.replace(microsecond=0)
     reason = event.pattern_match.group(1)
     pic = await event.client.download_media(reply) if reply else None
     if not USER_AFK:
         last_seen_status = await bot(
             functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
         )
         if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
             afk_time = datetime.datetime.now()
         USER_AFK = f"yes: {reason} {pic}"
         if reason:
             try:
                 if pic.endswith((".tgs", ".webp")):
                     await event.client.send_message(event.chat_id, file=pic)
                     await event.client.send_message(
                         event.chat_id,
                         f"\n**✘ {owner} Has AFK **\n**✦҈͜͡➳ Because :** `{reason}`",
                     )
                 else:
                     await event.client.send_message(
                         event.chat_id,
                         f"\n**✘ {owner} Has AFK **\n**✦҈͜͡➳ Because :** `{reason}`",
                         file=pic,
                     )
             except BaseException:
                 await event.client.send_message(
                     event.chat_id,
                     f"\n**✘ {owner} Has AFK **\n**✦҈͜͡➳ Because :** `{reason}`",
                 )
         else:
             try:
                 if pic.endswith((".tgs", ".webp")):
                     await event.client.send_message(event.chat_id, file=pic)
                     await event.client.send_message(
                         event.chat_id, f"**✘ {owner} Has been AFK **"
                     )
                 else:
                     await event.client.send_message(
                         event.chat_id,
                         f"**✘ {owner} Has been AFK **",
                         file=pic,
                     )
             except BaseException:
                 await event.client.send_message(
                     event.chat_id, f"**✘ {owner} Has been AFK **"
                 )
         await event.delete()
         try:
             if reason and pic:
                 if pic.endswith((".tgs", ".webp")):
                     await event.client.send_message(BOTLOG_CHATID, file=pic)
                     await event.client.send_message(
                         BOTLOG_CHATID,
                         f"\n**✘ {owner} In AFK **\n**✦҈͜͡➳ Because :** `{reason}`",
                     )
                 else:
                     await event.client.send_message(
                         BOTLOG_CHATID,
                         f"\n**✘ {owner} In AFK **\n**✦҈͜͡➳ Because :** `{reason}`",
                         file=pic,
                     )
             elif reason:
                 await event.client.send_message(
                     BOTLOG_CHATID,
                     f"\n**✘ {owner} In AFK **\n**✦҈͜͡➳ Because :** `{reason}`",
                 )
             elif pic:
                 if pic.endswith((".tgs", ".webp")):
                     await event.client.send_message(BOTLOG_CHATID, file=pic)
                     await event.client.send_message(
                         BOTLOG_CHATID, f"\n**✘ {owner} Currently AFK **"
                     )
                 else:
                     await event.client.send_message(
                         BOTLOG_CHATID,
                         f"\n**✘ {owner} In AFK **",
                         file=pic,
                     )
             else:
                 await event.client.send_message(
                     BOTLOG_CHATID, f"\n**✘ {owner} Currently AFK **"
                 )
         except Exception as e:
             BOTLOG_CHATIDger.warn(str(e))


 CMD_HELP.update(
     {
         "afk": f"**Plugin : **`afk`\
         \n\n • **Syntax :** `{cmd}afk` <reason> can be <while replying to sticker/photo/gif/media>\
         \n • **Function : **Notifies that Master is disabled by displaying cool media when someone bookmarks or replies to one of your messages or dm.\
         \n\n • **Syntax :** `{cmd}off`\
         \n • **Function : **Notifies that Master is OFFLINE, and changes the last name to OFF \
     "
     }
 )