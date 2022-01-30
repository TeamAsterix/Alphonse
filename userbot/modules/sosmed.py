from telethon import events
 from telethon.errors.rpcerrorlist import YouBlockedUserError
 from telethon.tl.functions.contacts import UnblockRequest
 from telethon.tl.functions.messages import DeleteHistoryRequest

 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP
 from userbot.utils import edit_delete, edit_or_reply, alphonse_cmd


 @alphonse_cmd(pattern="sosmed(?: |$)(.*)")
 async def insta(event):
     xxnx = event.pattern_match.group(1)
     if xxnx:
         link = xxnx
     elif event.is_reply:
         link = await event.get_reply_message()
     else:
         return await edit_delete(
             events,
             "**Give a Social Media Link or Reply a Social Media Link to Download**",
         )
     xx = await edit_or_reply(event, "`Processing Download...`")
     chat = "@SaveAsbot"
     async with event.client.conversation(chat) as conv:
         try:
             response = conv.wait_event(
                 events.NewMessage(incoming=True, from_users=523131145)
             )
             await event.client.send_message(chat, link)
             response = wait response
         except YouBlockedUserError:
             await event.client(UnblockRequest(chat))
             await event.client.send_message(chat, link)
             response = wait response
         if response.text.startswith("Forward"):
             await xx.edit("Forward Private .")
         else:
             await xx.delete()
             await event.client.send_file(
                 event.chat_id,
                 response.message.media,
             )
             await event.client.send_read_acknowledge(conv.chat_id)
             await event.client(DeleteHistoryRequest(peer=chat, max_id=0))
             await xx.delete()


 @alphonse_cmd(pattern="dez(?: |$)(.*)")
 async def DeezLoader(event):
     if event.fwd_from:
         return
     dlink = event.pattern_match.group(1)
     if ".com" not in dlink:
         await edit_delete(
             event, "`Please provide the link of the Deezloader you want to download`"
         )
     else:
         await edit_or_reply(event, "`Downloading Song...`")
     chat = "@DeezLoadBot"
     async with event.client.conversation(chat) as conv:
         try:
             await conv.send_message("/start")
             await conv.get_response()
             await conv.get_response()
             await conv.send_message(dlink)
             details = await conv.get_response()
             song = await conv.get_response()
             await event.client.send_read_acknowledge(conv.chat_id)
         except YouBlockedUserError:
             await event.client(UnblockRequest(chat))
             await conv.send_message("/start")
             await conv.get_response()
             await conv.get_response()
             await conv.send_message(dlink)
             details = await conv.get_response()
             song = await conv.get_response()
             await event.client.send_read_acknowledge(conv.chat_id)
         await event.client.send_file(event.chat_id, song, caption=details.text)
         await event.delete()


 CMD_HELP.update(
     {
         "sosmed": f"**Plugins : **`sosmed`\
         \n\n • **Syntax :** `{cmd}sosmed` <link>\
         \n • **Function : **Download Media From Pinterest / Tiktok / Instagram.\
         \n\n • **Syntax :** `{cmd}dez` <link>\
         \n • **Function : **Download Songs Via Deezloader\
     "
     }
 )