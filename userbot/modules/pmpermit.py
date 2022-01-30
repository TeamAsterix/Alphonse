""" Userbot module for keeping control who PM you. """

 from sqlalchemy.exc import IntegrityError
 from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
 from telethon.tl.functions.messages import ReportSpamRequest
 from telethon.tl.types import User

 from userbot import BOTLOG_CHATID
 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP, COUNT_PM, LASTMSG, LOGS, PM_AUTO_BAN, PM_LIMIT, bot
 from userbot.events import alphonse_cmd, register
 from userbot.utils import edit_delete, edit_or_reply

 DEF_UNAPPROVED_MSG = (
     "╔════════════════════╗\n"
     " \n"
     "╚════════════════════╝\n"
     "• I have not approved you to PM.\n"
     "• Wait until I approve your PM.\n"
     "• Don't Spam Chat or you will be automatically blocked.\n"
     "╔════════════════════╗\n"
     "    A L P H O N S E \n"
     "╚════════════════════╝\n"
 )


 @register(incoming=True, disable_edited=True, disable_errors=True)
 async def permitpm(event):
     """ Prohibits people from PMing you without approval. \
         Will block retarded nibbas automatically.  """
     if not PM_AUTO_BAN:
         return
     self_user = await event.client.get_me()
     sender = await event.get_sender()
     if (
         event.is_private
         and event.chat_id != 777000
         and event.chat_id != self_user.id
         and not sender.bot
         and not sender.contact
     ):
         try:
             from userbot.modules.sql_helper.globals import gvarstatus
             from userbot.modules.sql_helper.pm_permit_sql import is_approved
         except AttributeError:
             return
         apprv = is_approved(event.chat_id)
         notifsoff = gvarstatus("NOTIF_OFF")

         # Use user custom unapproved message
         getmsg = gvarstatus("unapproved_msg")
         UNAPPROVED_MSG = getmsg if getmsg is not None else DEF_UNAPPROVED_MSG
         # This part basically is a sanitation check
         # If the message that sent before is Unapproved Message
         # then stop sending it again to prevent FloodHit
         if not apprv and event.text != UNAPPROVED_MSG:
             if event.chat_id in LASTMSG:
                 prevmsg = LASTMSG[event.chat_id]
                 # If the message doesn't the same as previous one
                 # Send the Unapproved Message again
                 if event.text != prevmsg:
                     async for message in event.client.iter_messages(
                         event.chat_id, from_user="me", search=UNAPPROVED_MSG
                     ):
                         await message.delete()
                     await event.reply(f"{UNAPPROVED_MSG}")
             else:
                 await event.reply(f"{UNAPPROVED_MSG}")
             LASTMSG.update({event.chat_id: event.text})
             if notifsoff:
                 await event.client.send_read_acknowledge(event.chat_id)
             if event.chat_id not in COUNT_PM:
                 COUNT_PM.update({event.chat_id: 1})
             else:
                 COUNT_PM[event.chat_id] = COUNT_PM[event.chat_id] + 1

             if COUNT_PM[event.chat_id] > PM_LIMIT:
                 await event.respond(
                     "**Sorry You Have Been Blocked For Spam Chat**"
                 )

                 try:
                     del COUNT_PM[event.chat_id]
                     del LASTMSG[event.chat_id]
                 except KeyError:
                     if BOTLOG_CHATID:
                         await event.client.send_message(
                             BOTLOG_CHATID,
                             "**An error occurred while calculating the private message, please restart the bot!**",
                         )
                     return LOGS.info("Failed to count received PM")

                 await event.client(BlockRequest(event.chat_id))
                 await event.client(ReportSpamRequest(peer=event.chat_id))

                 if BOTLOG_CHATID:
                     name = await event.client.get_entity(event.chat_id)
                     name0 = str(name.first_name)
                     await event.client.send_message(
                         BOTLOG_CHATID,
                         "["
                         + name0
                         + "](tg://user?id="
                         + str(event.chat_id)
                         + ")"
                         + " **Blocked Due to Spam To Chat Room**",
                     )


 @register(disable_edited=True, outgoing=True, disable_errors=True)
 async def auto_accept(event):
     """Will approve automatically if you texted them first."""
     if not PM_AUTO_BAN:
         return
     self_user = await event.client.get_me()
     sender = await event.get_sender()
     if (
         event.is_private
         and event.chat_id != 777000
         and event.chat_id != self_user.id
         and not sender.bot
         and not sender.contact
     ):
         try:
             from userbot.modules.sql_helper.globals import gvarstatus
             from userbot.modules.sql_helper.pm_permit_sql import approve, is_approved
         except AttributeError:
             return

         # Use user custom unapproved message
         get_message = gvarstatus("unapproved_msg")
         UNAPPROVED_MSG = get_message if get_message is not None else DEF_UNAPPROVED_MSG
         chat = await event.get_chat()
         if isinstance(chat, User):
             if is_approved(event.chat_id) or chat.bot:
                 return
             async for message in event.client.iter_messages(
                 event.chat_id, reverse=True, limit=1
             ):
                 if (
                     message.text is not UNAPPROVED_MSG
                     and message.sender_id == self_user.id
                 ):
                     try:
                         approve(event.chat_id)
                     except IntegrityError:
                         return

                 if is_approved(event.chat_id) and BOTLOG_CHATID:
                     await event.client.send_message(
                         BOTLOG_CHATID,
                         "**#AUTO_APPROVED**\n"
                         + "👤 **User:** "
                         + f"[{chat.first_name}](tg://user?id={chat.id})",
                     )


 @bot.on(alphonse_cmd(outgoing=True, pattern=r"notifoff$"))
 async def notifoff(noff_event):
     """For .notifoff command, stop getting notifications from unapproved PMs."""
     try:
         from userbot.modules.sql_helper.globals import addgvar
     except AttributeError:
         return await noff_event.edit("`Running on Non-SQL mode!`")
     addgvar("NOTIF_OFF", True)
     await off_event.edit(
         "**Private Message Notification Disapproved, Has Been Muted!**"
     )


 @bot.on(alphonse_cmd(outgoing=True, pattern=r"notifon$"))
 async def notifon(non_event):
     """For .notifoff command, get notifications from unapproved PMs."""
     try:
         from userbot.modules.sql_helper.globals import delgvar
     except AttributeError:
         return await non_event.edit("`Running on Non-SQL mode!`")
     delgvar("NOTIF_OFF")
     await non_event.edit(
         "**Private Message Notification Approved, No Longer Mute!**"
     )


 @bot.on(alphonse_cmd(outgoing=True, pattern=r"(?:agree|ok)\s?(.)?"))
 async def approvepm(apprvpm):
     """For .ok command, give someone the permissions to PM you."""
     try:
         from userbot.modules.sql_helper.globals import gvarstatus
         from userbot.modules.sql_helper.pm_permit_sql import approve
     except AttributeError:
         return await edit_delete(apprvpm, "`Running on Non-SQL mode!`")

     if apprvpm.reply_to_msg_id:
         reply = await apprvpm.get_reply_message()
         replied_user = await apprvpm.client.get_entity(reply.sender_id)
         uid = replied_user.id
         name0 = str(replied_user.first_name)

     elif apprvpm.pattern_match.group(1):
         inputArgs = apprvpm.pattern_match.group(1)

         try:
             inputArgs = int(inputArgs)
         except ValueError:
             pass

         try:
             user = await apprvpm.client.get_entity(inputArgs)
         except BaseException:
             return await edit_delete(apprvpm, "**Invalid username/ID.**")

         if not isinstance(user, User):
             return await edit_delete(
                 apprvpm, "**Please Reply User Message You want to receive.**"
             )

         uid = user.id
         name0 = str(user.first_name)

     else:
         aname = await apprvpm.client.get_entity(apprvpm.chat_id)
         if not isinstance(aname, User):
             return await edit_delete(
                 apprvpm, "**Please Reply User Message You want to receive.**"
             )
         name0 = str(aname.first_name)
         uid = apprvpm.chat_id

     # Get user custom msg
     getmsg = gvarstatus("unapproved_msg")
     UNAPPROVED_MSG = getmsg if getmsg is not None else DEF_UNAPPROVED_MSG
     async for message in apprvpm.client.iter_messages(
         apprvpm.chat_id, from_user="me", search=UNAPPROVED_MSG
     ):
         await message.delete()

     try:
         approve(uid)
     except IntegrityError:
         return await edit_delete(apprvpm, "**Your Message Has Been Received**")

     await edit_delete(
         apprvpm, f"**Receiving Message From** [{name0}](tg://user?id={uid})", 5
     )


 @bot.on(alphonse_cmd(outgoing=True, pattern=r"(?:deny|nopm)\s?(.)?"))
 async def disapprovepm(disapprvpm):
     try:
         from userbot.modules.sql_helper.pm_permit_sql import dissprove
     except BaseException:
         return await edit_delete(disapprvpm, "`Running on Non-SQL mode!`")

     if disapprvpm.reply_to_msg_id:
         reply = await disapprvpm.get_reply_message()
         replied_user = await disapprvpm.client.get_entity(reply.sender_id)
         name = replied_user.id
         name0 = str(replied_user.first_name)
         dissprove(name)

     elif disapprvpm.pattern_match.group(1):
         inputArgs = disapprvpm.pattern_match.group(1)

         try:
             inputArgs = int(inputArgs)
         except ValueError:
             pass

         try:
             user = await disapprvpm.client.get_entity(inputArgs)
         except BaseException:
             return await edit_delete(
                 disapprvpm, "**Please reply to the message of the user you want to reject.**"
             )

         if not isinstance(user, User):
             return await edit_delete(
                 disapprvpm, "**Please reply to the message of the user you want to reject.**"
             )

         name = user.id
         dissprove(name)
         name0 = str(user.first_name)

     else:
         dissprove(disapprvpm.chat_id)
         aname = await disapprvpm.client.get_entity(disapprvpm.chat_id)
         if not isinstance(aname, User):
             return await edit_delete(
                 disapprvpm, "**This can be done only with users.**"
             )
         name0 = str(aname.first_name)
         aname = aname.id

     await edit_or_reply(
         disapprvpm,
         f" **Sorry Message** [{name0}](tg://user?id={aname}) **Rejected, Please Don't Spam the Chat Room!**",
     )


 @bot.on(alphonse_cmd(outgoing=True, pattern=r"block$"))
 async def blockpm(block):
     """For .block command, block people from PMing you!"""
     if block.reply_to_msg_id:
         reply = await block.get_reply_message()
         replied_user = await block.client.get_entity(reply.sender_id)
         name = replied_user.id
         await block.client(BlockRequest(aname))
         await block.edit("**You Have Been Blocked!**")
         uid = replied_user.id
     else:
         await block.client(BlockRequest(block.chat_id))
         aname = await block.client.get_entity(block.chat_id)
         if not isinstance(aname, User):
             return await block.edit("**This can be done only with users.**")
         await block.edit("**You Have Been Blocked!**")
         uid = block.chat_id

     try:
         from userbot.modules.sql_helper.pm_permit_sql import dissprove

         dissprove(uid)
     except AttributeError:
         pass


 @bot.on(alphonse_cmd(outgoing=True, pattern=r"unblock$"))
 async def unblockpm(unblock):
     """For .unblock command, let people PMing you again!"""
     if unblock.reply_to_msg_id:
         reply = await unblock.get_reply_message()
         replied_user = await unblock.client.get_entity(reply.sender_id)
         await unblock.client(UnblockRequest(replied_user.id))
         await unblock.edit("**You are No Longer Blocked.**")


 @bot.on(alphonse_cmd(outgoing=True, pattern=r"(set|get|reset) pmpermit(?: |$)(\w*)"))
 async def add_pmsg(cust_msg):
     """Set your own Unapproved message"""
     if not PM_AUTO_BAN:
         return await cust_msg.edit(
             "**You Must Set Var** `PM_AUTO_BAN` **To** `True`\n\n**If you want to Enable PMPERMIT Please Type:** `.set var PM_AUTO_BAN True`"
         )
     try:
         import userbot.modules.sql_helper.globals as sql
     except AttributeError:
         await cust_msg.edit("**Running on Non-SQL mode!**")
         return

     await cust_msg.edit("`Processing...`")
     conf = cust_msg.pattern_match.group(1)

     custom_message = sql.gvarstatus("unapproved_msg")

     if conf.lower() == "set":
         message = await cust_msg.get_reply_message()
         status = "Message"

         # check and clear user unapproved message first
         if custom_message is not None:
             sql.delgvar("unapproved_msg")
             status = "Message"

         if not message:
             return await cust_msg.edit("**Please reply to message**")

         # TODO: allow user to have a custom text formatting
         # eg: bold, underline, strikethrough, link
         # for now all text are in monoscape
         msg = message.message # get the plain text
         sql.addgvar("unapproved_msg", msg)
         await cust_msg.edit("**Message Saved Successfully To Room Chat**")

         if BOTLOG_CHATID:
             await cust_msg.client.send_message(
                 BOTLOG_CHATID,
                 f"**{status} Saved PMPERMIT:** \n\n{msg}",
             )

     if conf.lower() == "reset":
         if custom_message is None:
             await cust_msg.edit(
                 "`You've Deleted PMPERMIT Custom Message to Default`"
             )

         else:
             sql.delgvar("unapproved_msg")
             await cust_msg.edit("`Your PMPERMIT message was default from the start`")
     if conf.lower() == "get":
         if custom_message is not None:
             await cust_msg.edit(
                 "**Current PMPERMIT Message:**" f"\n\n{custom_message}"
             )
         else:
             await cust_msg.edit(
                 "**You Have Not Set PMPERMIT Custom Message,**\n"
                 f"**Still Using Default PM Message:**\n\n{DEF_UNAPPROVED_MSG}"
             )


 CMD_HELP.update(
     {
         "pmpermit": f"**Plugin : **`pmpermit`\
         \n\n • **Syntax :** `{cmd}agree` or `{cmd}ok`\
         \n • **Function : **Receive someone's message by replying to his message or tagging and also to do it in pm.\
         \n\n • **Syntax :** `{cmd}deny` or `{cmd}nopm`\
         \n • **Function : **Reject someone's message by replying to the message or tagging it and also doing it in pm.\
         \n\n • **Syntax :** `{cmd}block`\
         \n • **Function : **Blocking People in PM.\
         \n\n • **Syntax :** `{cmd}unblock`\
         \n • **Function : **Unblock.\
         \n\n • **Syntax :** `{cmd}notifoff`\
         \n • **Function : **Turn on notification of messages that have not been received.\
         \n\n • **Syntax :** `{cmd}notifon`\
         \n • **Function : **Turn on notification of messages that have not been received.\
         \n\n • **Syntax :** `{cmd}set pmermit` <reply to message>\
         \n • **Function : **Set your Private Message for people whose messages have not been received.\
         \n\n • **Syntax :** `{cmd}get pmermit`\
         \n • **Function : **Get your custom PM message.\
         \n\n • **Syntax :** `{cmd}reset pmermit`\
         \n • **Function : **Deletes PM messages to default.\
         \n\n • **Private Messages that have not been received at this time cannot be set to bold, underline, link, etc. rich format text.  Messages will be sent normally**\
         \n\n**NOTE: If you want to enable PMPERMIT Please Type:** `.set var PM_AUTO_BAN True`\
     "
     }
 )