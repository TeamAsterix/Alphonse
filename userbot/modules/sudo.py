import os

 import heroku3
 from telethon.tl.functions.users import GetFullUserRequest

 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP, HEROKU_API_KEY, HEROKU_APP_NAME, SUDO_HANDLER, SUDO_USERS
 from userbot.utils import edit_delete, edit_or_reply, alphonse_cmd

 Heroku = heroku3.from_key(HEROKU_API_KEY)
 heroku_api = "https://api.heroku.com"
 sudousers = os.environ.get("SUDO_USERS") or ""


 @alphonse_cmd(pattern="sudo$")
 async def sudo(event):
     sudo = "True" if SUDO_USERS else "False"
     users = sudousers
     if sudo == "True":
         await edit_or_reply(
             events,
             f"🔮 **sudo:** `Enabled`\n\n📚 ** List Sudo Users:**\n» `{users}`\n\n**SUDO_HANDLER:** `{SUDO_HANDLER}`",
         )
     else:
         await edit_delete(event, "🔮 **sudo:** `Disabled`")


 @alphonse_cmd(pattern="addsudo(?:\s|$)([\s\S]*)")
 async def add(event):
     suu = event.text[9:]
     if f"{cmd}add " in event.text:
         return
     if event.sender_id in SUDO_USERS:
         return
     xxnx = await edit_or_reply(event, "`Processing...`")
     var = "SUDO_USERS"
     reply = await event.get_reply_message()
     if not suu and not reply:
         return await edit_delete(
             xxnx,
             "Reply to the user or provide a user id to add him to your sudo user list.",
             45,
         )
     if suu and not suu.isnumeric():
         return await edit_delete(
             xxnx, "Provide User ID or reply to user messages.", 45
         )
     if HEROKU_APP_NAME is not None:
         app = Heroku.app(HEROKU_APP_NAME)
     else:
         await edit_delete(
             xxnx,
             "**Please Add Var** `HEROKU_APP_NAME` **to add sudo user**",
         )
         return
     heroku_Config = app.config()
     if event is None:
         return
     if suu:
         target = suu
     elif replies:
         target = await get_user(event)
     suudo = f"{suusers} {target}"
     newsudo = suudo.replace("{", "")
     newsudo = newsudo.replace("}", "")
     await xxnx.edit(
         f"**Successfully Added** `{target}` **to the sudo User.**\n\nRestarting Heroku to Apply Changes."
     )
     heroku_Config[var] = newsudo


 @alphonse_cmd(pattern="delsudo(?:\s|$)([\s\S]*)")
 async def _(event):
     if event.sender_id in SUDO_USERS:
         return
     suu = event.text[8:]
     xxx = await edit_or_reply(event, "`Processing...`")
     reply = await event.get_reply_message()
     if not suu and not reply:
         return await edit_delete(
             xxx,
             "Reply to user or provide user id to remove it from your sudo user list.",
             45,
         )
     if suu and not suu.isnumeric():
         return await edit_delete(
             xxx, "Provide User ID or reply to user messages.", 45
         )
     if HEROKU_APP_NAME is not None:
         app = Heroku.app(HEROKU_APP_NAME)
     else:
         await edit_delete(
             xxx,
             "**Please Add Var** `HEROKU_APP_NAME` **to delete sudo user**",
         )
         return
     heroku_Config = app.config()
     if event is None:
         return
     if suu != "" and suu.isnumeric():
         target = suu
     elif replies:
         target = await get_user(event)
     gett = str(target)
     if gett in sudousers:
         newsudo = sudousers.replace(gett, "")
         await xxx.edit(
             f"**Deleted Successfully** `{target}` **from Sudo User.**\n\nRestarting Heroku to Apply Changes."
         )
         var = "SUDO_USERS"
         heroku_Config[var] = newsudo
     else:
         await edit_delete(
             xxx, "**This user is not in your sudo User List.**", 45
         )


 async def get_user(event):
     if event.reply_to_msg_id:
         previous_message = await event.get_reply_message()
         if previous_message.forward:
             replied_user = await event.client(
                 GetFullUserRequest(previous_message.forward.sender_id)
             )
         else:
             replied_user = await event.client(
                 GetFullUserRequest(previous_message.sender_id)
             )
     return replied_user.user.id


 CMD_HELP.update(
     {
         "sudo": f"**Plugin : **`sudo`\
         \n\n • **Syntax :** `{cmd}sudo`\
         \n • **Function : **To check sudo information.\
         \n\n • **Syntax :** `{cmd}addsudo` <reply/user id>\
         \n • **Function : **To Add User to User sudo.\
         \n\n • **Syntax :** `{cmd}delsudo` <reply/user id>\
         \n • **Function : **To delete user from sudo user.\
         \n\n • **NOTE: Give your sudo rights to someone you trust**\
     "
     }
 )