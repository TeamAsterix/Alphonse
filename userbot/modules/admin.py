import logging
 from asyncio import sleep

 from telethon.errors import (
     BadRequestError,
     ImageProcessFailedError,
     PhotoCropSizeSmallError,
 )
 from telethon.errors.rpcerrorlist import (
     ChatAdminRequiredError,
     UserAdminInvalidError,
     UserIdInvalidError,
 )
 from telethon.tl.functions.channels import (
     EditAdminRequest,
     EditBannedRequest,
     EditPhotoRequest,
 )
 from telethon.tl.functions.users import GetFullUserRequest
 from telethon.tl.types import (
     ChannelParticipantsAdmins,
     ChatAdminRights,
     ChatBannedRights,
     InputChatPhotoEmpty,
     MessageMediaPhoto,
 )

 from userbot import BOTLOG_CHATID
 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP, DEVS, owner
 from userbot.events import register
 from userbot.utils import (
     _format,
     edit_delete,
     edit_or_reply,
     get_user_from_event,
     alphonse_cmd,
     alphonse_handler,
     media_type,
 )

 # =================== CONSTANT ===================
 PP_TOO_SMOL = "**Image Too Small**"
 PP_ERROR = "**Failed to Process Image**"
 NO_ADMIN = "**Failed because Not Admin :)**"
 NO_PERM = "**No Permissions!**"
 NO_SQL = "**Running In Non-SQL Mode**"
 CHAT_PP_CHANGED = "**Change Group Profile Successfully**"
 INVALID_MEDIA = "**Invalid Media**"

 BANNED_RIGHTS = ChatBannedRights(
     until_date=None,
     view_messages=True,
     send_messages=True,
     send_media=True,
     send_stickers=True,
     send_gifs=True,
     send_games=True,
     send_inline=True,
     embed_links=True,
 )

 UNBAN_RIGHTS = ChatBannedRights(
     until_date=None,
     send_messages=None,
     send_media=None,
     send_stickers=None,
     send_gifs=None,
     send_games=None,
     send_inline=None,
     embed_links=None,
 )
 logging.basicConfig(
     format="[%(levelname)s- %(asctime)s]- %(name)s- %(message)s",
     level=logging.INFO,
     datefmt="%H:%M:%S",
 )

 LOGS = logging.getLogger(__name__)
 MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
 UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
 # ================================================


 @alphonse_cmd(pattern="setgpic( -s| -d)$")
 @register(pattern=r"^\.csetgpic( -s| -d)$", sudo=True)
 async def set_group_photo(event):
     "For changing groups dp"
     flag = (event.pattern_match.group(1)).strip()
     if flags == "-s":
         replymsg = await event.get_reply_message()
         photo = None
         if replymsg and replymsg.media:
             if isinstance(replymsg.media, MessageMediaPhoto):
                 photo = await event.client.download_media(message=replymsg.photo)
             elif "image" in replymsg.media.document.mime_type.split("/"):
                 photo = await event.client.download_file(replymsg.media.document)
             else:
                 return await edit_delete(event, INVALID_MEDIA)
         if photo:
             try:
                 await event.client(
                     EditPhotoRequest(
                         event.chat_id, await event.client.upload_file(photo)
                     )
                 )
                 await edit_delete(event, CHAT_PP_CHANGED)
             except PhotoCropSizeSmallError:
                 return await edit_delete(event, PP_TOO_SMOL)
             except ImageProcessFailedError:
                 return await edit_delete(event, PP_ERROR)
             except Exception as e:
                 return await edit_delete(event, f"**ERROR : **`{str(e)}`")
     else:
         try:
             await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
         except Exception as e:
             return await edit_delete(event, f"**ERROR : **`{e}`")
         await edit_delete(event, "**Group Profile Photo successfully deleted.**", 30)


 @alphonse_cmd(pattern="promote(?:\s|$)([\s\S]*)")
 @register(pattern=r"^\.cpromote(?:\s|$)([\s\S]*)", sudo=True)
 async def promote(event):
     new_rights = ChatAdminRights(
         add_admins=False,
         change_info=True,
         invite_users=True,
         ban_users=True,
         delete_messages=True,
         pin_messages=True,
         manage_call=True,
     )
     user, rank = await get_user_from_event(event)
     if not rank:
         rank = "admin"
     if not user:
         return
     eventman = await edit_or_reply(event, "`Promoting...`")
     try:
         await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
     except BadRequestError:
         return await eventman.edit(NO_PERM)
     await edit_delete(eventman, "`Promoted Successfully!`", 30)


 @alphonse_cmd(pattern="demote(?:\s|$)([\s\S]*)")
 @register(pattern=r"^\.cdemote(?:\s|$)([\s\S]*)", sudo=True)
 async def demote(event):
     "To demote a person in group"
     user, _ = await get_user_from_event(event)
     if not user:
         return
     eventman = await edit_or_reply(event, "`Demoting...`")
     newrights = ChatAdminRights(
         add_admins=None,
         invite_users=None,
         change_info=None,
         ban_users=None,
         delete_messages=None,
         pin_messages=None,
         manage_call=None,
     )
     rank = "admin"
     try:
         await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
     except BadRequestError:
         return await eventman.edit(NO_PERM)
     await edit_delete(eventman, "`Demoted Successfully!`", 30)


 @alphonse_cmd(pattern="ban(?:\s|$)([\s\S]*)")
 @register(pattern=r"^\.cban(?:\s|$)([\s\S]*)", sudo=True)
 async def ban(bon):
     chat = await bon.get_chat()
     admin = chat.admin_rights
     creator = chat.creator
     if not admin and not creator:
         return await edit_or_reply(bon, NO_ADMIN)

     user, reason = await get_user_from_event(bon)
     if not user:
         return
     await edit_or_reply(bon, "`Processing Banned...`")
     try:
         await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
     except BadRequestError:
         return await edit_or_reply(bon, NO_PERM)
     if reason:
         await edit_or_reply(
             bill,
             r"\\**#Banned_User**//"
             f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
             f"**User ID:** `{str(user.id)}`\n"
             f"**Reason:** `{reason}`",
         )
     else:
         await edit_or_reply(
             bill,
             f"\\\\**#Banned_User**//\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n*  *User ID:** `{user.id}`\n**Action:** `Banned User by {owner}`",
         )


 @alphonse_cmd(pattern="unban(?:\s|$)([\s\S]*)")
 @register(pattern=r"^\.cunban(?:\s|$)([\s\S]*)", sudo=True)
 async def nothanos(unbon):
     chat = await unbon.get_chat()
     admin = chat.admin_rights
     creator = chat.creator
     if not admin and not creator:
         return await edit_delete(unbon, NO_ADMIN)
     await edit_or_reply(unbon, "`Processing...`")
     user = await get_user_from_event(unbon)
     user = user[0]
     if not user:
         return
     try:
         await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
         await edit_delete(unbon, "`Unban Successfully Done!`")
     except UserIdInvalidError:
         await edit_delete(unbon, "`There seems to be an ERROR!`")


 @alphonse_cmd(pattern="mute(?: |$)(.*)")
 @register(pattern=r"^\.cmute(?: |$)(.*)", sudo=True)
 async def spider(spdr):
     try:
         from userbot.modules.sql_helper.spam_mute_sql import mute
     except AttributeError:
         return await edit_or_reply(spdr, NO_SQL)
     chat = await spdr.get_chat()
     admin = chat.admin_rights
     creator = chat.creator
     if not admin and not creator:
         return await edit_or_reply(spdr, NO_ADMIN)
     user, reason = await get_user_from_event(spdr)
     if not user:
         return
     self_user = await spdr.client.get_me()
     if user.id == self_user.id:
         return await edit_or_reply(
             spdr, "**Can't Mute Myself..（>﹏<）**"
         )
     if user.id in DEVS:
         return await edit_or_reply(spdr, "**Mute Failed, He Is My Maker **")
     await edit_or_reply(
         spdr,
         r"\\**#Muted_User**//"
         f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
         f"**User ID:** `{user.id}`\n"
         f"**Action:** `Mute by {owner}`",
     )
     if mute(spdr.chat_id, user.id) is False:
         return await edit_delete(spdr, "**ERROR:** `User Muted.`")
     try:
         await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))
         if reason:
             await edit_or_reply(
                 spdr,
                 r"\\**#DMute_User**//"
                 f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
                 f"**User ID:** `{user.id}`\n"
                 f"**Reason:** `{reason}`",
             )
         else:
             await edit_or_reply(
                 spdr,
                 r"\\**#DMute_User**//"
                 f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
                 f"**User ID:** `{user.id}`\n"
                 f"**Action:** `DMute by {owner}`",
             )
     except UserIdInvalidError:
         return await edit_delete(spdr, "**An ERROR occurred!**")


 @alphonse_cmd(pattern="unmute(?: |$)(.*)")
 @register(pattern=r"^\.cunmute(?: |$)(.*)", sudo=True)
 async def unmoot(unmot):
     chat = await unmot.get_chat()
     admin = chat.admin_rights
     creator = chat.creator
     if not admin and not creator:
         return await edit_delete(unmot, NO_ADMIN)
     try:
         from userbot.modules.sql_helper.spam_mute_sql import unmute
     except AttributeError:
         return await unmot.edit(NO_SQL)
     await edit_or_reply(unmot, "`Processing...`")
     user = await get_user_from_event(unmot)
     user = user[0]
     if not user:
         return

     if unmute(unmot.chat_id, user.id) is False:
         return await edit_delete(unmot, "**ERROR! User Unmuted.**")
     try:
         await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
         await edit_delete(unmot, "**Unmute Successfully!**")
     except UserIdInvalidError:
         return await edit_delete(unmot, "**An ERROR occurred!**")


 @alphonse_handler()
 async def muter(moot):
     try:
         from userbot.modules.sql_helper.gmute_sql import is_gmuted
         from userbot.modules.sql_helper.spam_mute_sql import is_muted
     except AttributeError:
         return
     muted = is_muted(moot.chat_id)
     gmuted = is_gmuted(moot.sender_id)
     rights = ChatBannedRights(
         until_date=None,
         send_messages=True,
         send_media=True,
         send_stickers=True,
         send_gifs=True,
         send_games=True,
         send_inline=True,
         embed_links=True,
     )
     if muted:
         for i in muted:
             if str(i.sender) == str(moot.sender_id):
                 await moot.delete()
                 await moot.client(
                     EditBannedRequest(moot.chat_id, moot.sender_id, rights)
                 )
     for i in gmuted:
         if i.sender == str(moot.sender_id):
             await moot.delete()


 @alphonse_cmd(pattern="ungmute(?: |$)(.*)")
 @register(pattern=r"^\.cungmute(?: |$)(.*)", sudo=True)
 async def ungmoot(un_gmute):
     chat = await un_gmute.get_chat()
     admin = chat.admin_rights
     creator = chat.creator
     if not admin and not creator:
         return await edit_delete(un_gmute, NO_ADMIN)
     try:
         from userbot.modules.sql_helper.gmute_sql import ungmute
     except AttributeError:
         return await edit_delete(un_gmute, NO_SQL)
     user = await get_user_from_event(un_gmute)
     user = user[0]
     if not user:
         return
     await edit_or_reply(un_gmute, "`Unlocking User Global Mute...`")
     if ungmute(user.id) is False:
         await un_gmute.edit("**ERROR!** User Not Gmuteed.")
     else:
         await edit_delete(un_gmute, "**Success! User Unmuted**")


 @alphonse_cmd(pattern="gmute(?: |$)(.*)")
 @register(pattern=r"^\.cgmute(?: |$)(.*)", sudo=True)
 async def gspider(gspdr):
     chat = await gspdr.get_chat()
     admin = chat.admin_rights
     creator = chat.creator
     if not admin and not creator:
         return await edit_delete(gspdr, NO_ADMIN)
     try:
         from userbot.modules.sql_helper.gmute_sql import gmute
     except AttributeError:
         return await gspdr.edit(NO_SQL)
     user, reason = await get_user_from_event(gspdr)
     if not user:
         return
     self_user = await gspdr.client.get_me()
     if user.id == self_user.id:
         return await edit_or_reply(
             gspdr, "**Can't Mute Myself..（>﹏<）**"
         )
     if user.id in DEVS:
         return await edit_or_reply(
             gspdr, "**Failed Global Mute, He Is My Maker **"
         )
     await edit_or_reply(gspdr, "**Mute User Successfully!**")
     if gmute(user.id) is False:
         await edit_delete(gspdr, "**ERROR! User Muted.**")
     elif reason:
         await edit_or_reply(
             gspdr,
             r"\\**#GMuted_User**//"
             f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
             f"**User ID:** `{user.id}`\n"
             f"**Reason:** `{reason}`",
         )
     else:
         await edit_or_reply(
             gspdr,
             r"\\**#GMuted_User**//"
             f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
             f"**User ID:** `{user.id}`\n"
             f"**Action:** `Global Muted by {owner}`",
         )


 @alphonse_cmd(pattern="zombies(?: |$)(.*)")
 async def rm_deletedacc(show):
     con = show.pattern_match.group(1).lower()
     del_u = 0
     del_status = "**Clean Group, Couldn't Find Deleted Account.**"
     if con != "clean":
         await show.edit("`Looking for a Depression Account...`")
         async for user in show.client.iter_participants(show.chat_id):
             if user.deleted:
                 del_u += 1
                 wait sleep(1)
         if del_u > 0:
             del_status = (
                 f"**Found** `{del_u}` **Depression/Deleted/Zombie Accounts In This Group,"
                 "\nClean It Using Command** `.zombies clean`"
             )
         return await show.edit(del_status)
     chat = await show.get_chat()
     admin = chat.admin_rights
     creator = chat.creator
     if not admin and not creator:
         return await show.edit("**Sorry You Are Not Admin!**")
     await show.edit("`Deleting Depression Account...`")
     del_u = 0
     del_a = 0
     async for user in show.client.iter_participants(show.chat_id):
         if user.deleted:
             try:
                 await show.client(
                     EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS)
                 )
             except ChatAdminRequiredError:
                 return await show.edit("`No Banned Permissions In This Group`")
             except UserAdminInvalidError:
                 del_u -= 1
                 del_a += 1
             await show.client(EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
             del_u += 1
     if del_u > 0:
         del_status = f"**Cleaning** `{del_u}` **Deleted Account**"
     if del_a > 0:
         del_status = (
             f"**Cleaning** `{del_u}` **Deleted Account** "
             f"\n`{del_a}` **Deleted Admin Account Not Deleted.**"
         )
     await show.edit(del_status)
     wait sleep(2)
     await show.delete()
     if BOTLOG_CHATID:
         await show.client.send_message(
             BOTLOG_CHATID,
             "**#ZOMBIES**\n"
             f"**Cleaning** `{del_u}` **Deleted Account!**"
             f"\n**GROUP:** {show.chat.title}(`{show.chat_id}`)",
         )


 @alphonse_cmd(pattern="admins$")
 async def get_admin(show):
     info = await show.client.get_entity(show.chat_id)
     title = info.title or "This Group"
     mentions = f"<b>👑 Group Admin List {title}:</b> \n"
     try:
         async for user in show.client.iter_participants(
             show.chat_id, filter=ChannelParticipantsAdmins
         ):
             if not user.deleted:
                 link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                 mentions += f"\n⚜️ {link}"
             else:
                 mentions += f"\n⚜ Account Deleted <code>{user.id}</code>"
     except ChatAdminRequiredError as err:
         mentions += " " + str(err) + "\n"
     await show.edit(mentions, parse_mode="html")


 @alphonse_cmd(pattern="pin( loud|$)")
 @register(pattern=r"^\.cpin( loud|$)", sudo=True)
 async def pin(event):
     to_pin = event.reply_to_msg_id
     if not to_pin:
         return await edit_delete(event, "`Reply Message to Pin.`", 30)
     options = event.pattern_match.group(1)
     is_silent = bool(options)
     try:
         await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
     except BadRequestError:
         return await edit_delete(event, NO_PERM, 5)
     except Exception as e:
         return await edit_delete(event, f"`{e}`", 5)
     await edit_delete(event, "`Pinned Successfully!`")


 @alphonse_cmd(pattern="unpin( all|$)")
 @register(pattern=r"^\.cunpin( all|$)", sudo=True)
 async def pin(event):
     to_unpin = event.reply_to_msg_id
     options = (event.pattern_match.group(1)).strip()
     if not to_unpin and options != "all":
         return await edit_delete(
             events,
             "**Reply to Messages to unpin or Use** `.unpin all` **to unpin all**",
             45,
         )
     try:
         if to_unpin and not options:
             await event.client.unpin_message(event.chat_id, to_unpin)
         elif options == "all":
             await event.client.unpin_message(event.chat_id)
         else:
             return await edit_delete(
                 events,
                 "**Reply to Messages to unpin or use** `.unpin all`",
                 45,
             )
     except BadRequestError:
         return await edit_delete(event, NO_PERM, 5)
     except Exception as e:
         return await edit_delete(event, f"`{e}`", 5)
     await edit_delete(event, "`Unpinned Successfully!`")


 @alphonse_cmd(pattern="kick(?: |$)(.*)")
 @register(pattern=r"^\.ckick(?: |$)(.*)", sudo=True)
 async def kick(usr):
     chat = await usr.get_chat()
     admin = chat.admin_rights
     creator = chat.creator
     if not admin and not creator:
         return await edit_delete(usr, NO_ADMIN)
     user, reason = await get_user_from_event(usr)
     if not user:
         return await edit_delete(usr, "**Cannot Find User.**")
     xxnx = await edit_or_reply(usr, "`Processing...`")
     try:
         await usr.client.kick_participant(usr.chat_id, user.id)
         wait sleep(0.5)
     except Exception as e:
         return await edit_delete(usr, NO_PERM + f"\n{e}")
     if reason:
         await xxnx.edit(
             f"[{user.first_name}](tg://user?id={user.id}) **Kicked From Group**\n**Reason:** `{reason}`"
         )
     else:
         await xxnx.edit(
             f"[{user.first_name}](tg://user?id={user.id}) **Kicked From Group**",
         )


 @alphonse_cmd(pattern=r"undlt( -u)?(?: |$)(\d*)?")
 async def _iundlt(event):
     catevent = await edit_or_reply(event, "`Searching recent actions...`")
     flag = event.pattern_match.group(1)
     if event.pattern_match.group(2) != "":
         lim = int(event.pattern_match.group(2))
         if lim > 15:
             lim = int(15)
         if lim <= 0:
             lim = int(1)
     else:
         lim = int(5)
     adminlog = await event.client.get_admin_log(
         event.chat_id, limit=lim, edit=False, delete=True
     )
     deleted_msg = f"**{lim} Deleted messages in this group:**"
     if not flags:
         for msg in adminlog:
             rusers = (
                 await event.client(GetFullUserRequest(msg.old.from_id.user_id))
             ).user
             _media_type = media_type(msg.old)
             if _media_type is None:
                 deleted_msg += f"\n☞ __{msg.old.message}__ **Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}"
             else:
                 deleted_msg += f"\n☞ __{_media_type}__ **Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}"
         await edit_or_reply(catevent, deleted_msg)
     else:
         main_msg = await edit_or_reply(catevent, deleted_msg)
         for msg in adminlog:
             rusers = (
                 await event.client(GetFullUserRequest(msg.old.from_id.user_id))
             ).user
             _media_type = media_type(msg.old)
             if _media_type is None:
                 await main_msg.reply(
                     f"{msg.old.message}\n**Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                 )
             else:
                 await main_msg.reply(
                     f"{msg.old.message}\n**Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                     file=msg.old.media,
                 )


 CMD_HELP.update(
     {
         "admin": f"**Plugins : **`admin`\
         \n\n • **Syntax :** `{cmd}promote <username/reply> <title name (optional)>`\
         \n • **Function : **Promoting member as admin.\
         \n\n • **Syntax :** `{cmd}demote <username/reply to message>`\
         \n • **Function : **Decrease admin as a member.\
         \n\n • **Syntax :** `{cmd}ban <username/reply to message> <reason (optional)>`\
         \n • **Function : **Banned User from group.\
         \n\n • **Syntax :** `{cmd}unban <username/reply>`\
         \n • **Function : **Unbanned users so they can join groups again.\
         \n\n • **Syntax :** `{cmd}mute <username/reply> <reason (optional)>`\
         \n • **Function : **Mute Someone in the Group, Can Also Go to Admin.\
         \n\n • **Syntax :** `{cmd}unmute <username/reply>`\
         \n • **Function : **Unmute people who are muted.\
         \n • **Function : ** Unlock global mute people who are muted.\
         \n\n • **Syntax :** `{cmd}all`\
         \n • **Function : **Tag all members in the group.\
         \n\n • **Syntax :** `{cmd}admins`\
         \n • **Function : **View the list of admins in the group.\
         \n\n • **Syntax :** `{cmd}setgpic <flags> <reply to image>`\
         \n • **Function : **To change the group profile picture or delete the group profile picture.\
         \n • **Flags :** `-s` = **To change group photo** or `-d` = **To delete group photo**\
     "
     }
 )


 CMD_HELP.update(
     {
         "pin": f"**Plugin : **`pin`\
         \n\n • **Syntax :** `{cmd}pin` <reply chat>\
         \n • **Function : **To embed a message in a group.\
         \n\n • **Syntax :** `{cmd}pin loud` <reply chat>\
         \n • **Function : **To pin messages in groups (without notifications) / pin silently.\
         \n\n • **Syntax :** `{cmd}unpin` <reply chat>\
         \n • **Function : **To unpin messages in a group.\
         \n\n • **Syntax :** `{cmd}unpin all`\
         \n • **Function : **To unpin all messages in a group.\
     "
     }
 )


 CMD_HELP.update(
     {
         "undelete": f"**Plugin : **`undelete`\
         \n\n • **Syntax :** `{cmd}undlt` <number of chats>\
         \n • **Function : **To get recently deleted messages in a group\
         \n\n • **Syntax :** `{cmd}undlt -u` <number of chats>\
         \n • **Function : **To get recently deleted media messages in the \ group
         \n • **Flags :** `-u` = **Use these flags to upload media.**\
         \n\n • **NOTE : Requires Group admin rights** \
     "
     }
 )


 CMD_HELP.update(
     {
         "gmute": f"**Plugin : **`gmute`\
         \n\n • **Syntax :** `{cmd}gmute` <username/reply> <reason (optional)>\
         \n • **Function : **To Mute Users in all groups that you admin.\
         \n\n • **Syntax :** `{cmd}ungmute` <username/reply>\
         \n • **Function : **To open global mute Users in all groups that you admin.\
     "
     }
 )


 CMD_HELP.update(
     {
         "zombies": f"**Plugins : **`zombies`\
         \n\n • **Syntax :** `{cmd}zombies`\
         \n • **Function : **To find deleted accounts in a group\
         \n\n • **Syntax :** `{cmd}zombies clean`\
         \n • **Function : **to remove the Deleted Account from the group.\
     "
     }
 )