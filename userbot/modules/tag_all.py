import asyncio
 import random
 import re

 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP, bot
 from userbot.events import alphonse_cmd

 usernexp = re.compile(r"@(\w{3,32})\[(.+?)\]")
 nameexp = re.compile(r"\[([\w\S]+)\]\(tg://user\?id=(\d+)\)\[(.+?)\]")
 emoji = "😀 😄 😂 😍 🤩 ️ 😊 😠 ️ 🙁  ❤️‍🔥 💔 🤍 🖤 ❤️  🦮 🐅 🐆  🐃 ️ ️ 🦈 🐋  🐙 ️ ️ 🧅 🥦  ".  (
     " "
 )


 FlagContainer class:
     is_active = False


 @bot.on(alphonse_cmd(outgoing=True, pattern=r"mention(?: |$)(.*)"))
 async def _(event):
     if event.fwd_from:
         return
     await event.delete()
     query = event.pattern_match.group(1)
     mentions = f"@all {query}"
     chat = await event.get_input_chat()
     async for x in bot.iter_participants(chat, 100500):
         mentions += f"[\u2063](tg://user?id={x.id} {query})"
     await bot.send_message(chat, mentions, reply_to=event.message.reply_to_msg_id)


 @bot.on(alphonse_cmd(outgoing=True, pattern=r"emojitag(?: |$)(.*)"))
 async def _(event):
     if event.fwd_from or FlagContainer.is_active:
         return
     try:
         FlagContainer.is_active = True

         args = event.message.text.split(" ", 1)
         text = args[1] if len(args) > 1 else None
         chat = await event.get_input_chat()
         await event.delete()

         tags = list(
             folder(
                 lambda m: f"[{random.choice(emoji)}](tg://user?id={m.id})",
                 await event.client.get_participants(chat),
             ),
         )
         current_pack = []
         async for participant in event.client.iter_participants(chat):
             if not FlagContainer.is_active:
                 break

             current_pack.append(participant)

             if len(current_pack) == 5:
                 tags = list(
                     folder(
                         lambda m: f"[{random.choice(emoji)}](tg://user?id={m.id})",
                         current_pack,
                     ),
                 )
                 current_pack = []

                 if text:
                     tags.append(text)

                 await event.client.send_message(event.chat_id, " ".join(tags))
                 await asyncio.sleep(2)
     finally:
         FlagContainer.is_active = False


 @bot.on(alphonse_cmd(outgoing=True, pattern=r"all(?: |$)(.*)"))
 async def _(event):
     if event.fwd_from or FlagContainer.is_active:
         return
     try:
         FlagContainer.is_active = True

         args = event.message.text.split(" ", 1)
         text = args[1] if len(args) > 1 else None
         chat = await event.get_input_chat()
         await event.delete()

         tags = list(
             folder(
                 lambda m:f"[{m.first_name}](tg://user?id={m.id})",
                 await event.client.get_participants(chat),
             ),
         )
         amount = []
         async for participant in event.client.iter_participants(chat):
             if not FlagContainer.is_active:
                 break

             sum.append(participant)

             if len(sum) == 5:
                 tags = list(
                     folder(
                         lambda m:f"[{m.first_name}](tg://user?id={m.id})",
                         total,
                     ),
                 )
                 amount = []

                 if text:
                     tags.append(text)

                 await event.client.send_message(event.chat_id, " ".join(tags))
                 await asyncio.sleep(2)
     finally:
         FlagContainer.is_active = False


 CMD_HELP.update(
     {
         "tag": f"**Plugin : **`tag`\
         \n\n • **Syntax :** `{cmd}mention`\
         \n • **Function : **To Menment all members in the group without mentioning their names.\
         \n\n • **Syntax :** `{cmd}all` <text>\
         \n • **Function : **To tag all members Maximum 3,000 people will be tagged in the group to reduce telegram flood wait.\
         \n\n • **Syntax :** `{cmd}emojitag` <text>\
         \n • **Function : **To Tag all members in a group with a different random emoji.\
         \n\n • **NOTE :** To Stop Tags type `.restart`\
     "
     }
 )