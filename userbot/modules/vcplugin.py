# Credit - Ryoishin

 from pytgcalls import StreamType
 from pytgcalls.types import Update
 from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
 from pytgcalls.types.input_stream.quality import (
     HighQualityAudio,
     HighQualityVideo,
     LowQualityVideo,
     MediumQualityVideo,
 )
 from telethon.tl import types
 from telethon.utils import get_display_name
 from youtubesearchpython import VideosSearch

 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP
 from userbot import PLAY_PIC as fotoplay
 from userbot import QUEUE_PIC as ngantri
 from userbot import call_py, owner
 from userbot.utils import bash, edit_delete, edit_or_reply, alphonse_cmd
 from userbot.utils.chattitle import CHAT_TITLE
 from userbot.utils.queues.queues import (
     QUEUE,
     add_to_queue,
     clear_queue,
     get_queue,
     pop_an_item,
 )
 from userbot.utils.thumbnail import gen_thumb


 def vcmmention(user):
     full_name = get_display_name(user)
     if not isinstance(user, types.User):
         return full_name
     return f"[{full_name}](tg://user?id={user.id})"


 def ytsearch(query: str):
     try:
         search = VideosSearch(query, limit=1).result()
         data = search["result"][0]
         songname = data["title"]
         url = data["link"]
         duration = data["duration"]
         thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
         return [songname, url, duration, thumbnail]
     except Exception as e:
         print(e)
         return 0


 async def ytdl(format: str, link: str):
     stdout, stderr = await bash(f'yt-dlp -g -f "{format}" {link}')
     if stdout:
         return 1, stdout.split("\n")[0]
     return 0, stderr


 async def skip_item(chat_id: int, x: int):
     if chat_id not in QUEUE:
         return 0
     chat_queue = get_queue(chat_id)
     try:
         songname = chat_queue[x][0]
         chat_queue.pop(x)
         return songname
     except Exception as e:
         print(e)
         return 0


 async def skip_current_song(chat_id: int):
     if chat_id not in QUEUE:
         return 0
     chat_queue = get_queue(chat_id)
     if len(chat_queue) == 1:
         await call_py.leave_group_call(chat_id)
         clear_queue(chat_id)
         returns 1
     songname = chat_queue[1][0]
     url = chat_queue[1][1]
     link = chat_queue[1][2]
     type = chat_queue[1][3]
     RESOLUTION = chat_queue[1][4]
     if type == "Audio":
         await call_py.change_stream(
             chat_id,
             AudioPiped(
                 urls,
             ),
         )
     elif type == "Video":
         if RESOLUTION == 720:
             hm = HighQualityVideo()
         elif RESOLUTION == 480:
             hm = MediumQualityVideo()
         elif RESOLUTION == 360:
             hm = LowQualityVideo()
         await call_py.change_stream(
             chat_id, AudioVideoPiped(url, HighQualityAudio(), hm)
         )
     pop_an_item(chat_id)
     return [songname, link, type]


 @alphonse_cmd(pattern="play(?:\s|$)([\s\S]*)")
 async def vc_play(event):
     title = event.pattern_match.group(1)
     replied = await event.get_reply_message()
     sender = await event.get_sender()
     chat = await event.get_chat()
     chat_id = event.chat_id
     from_user = vcmention(event.sender)
     if (
         replied
         and not replied.audio
         and not replied.voice
         and not title
         or not replied
         and not title
     ):
         return await edit_or_reply(event, "**Please Enter Song Title**")
     elif replied and not replied.audio and not replied.voice or not replied:
         botman = await edit_or_reply(event, "`Searching...`")
         query = event.text.split(maxsplit=1)[1]
         search = ytsearch(query)
         if search == 0:
             await botman.edit(
                 "**Unable to Find Song** Try searching with a More Specific Title"
             )
         else:
             songname = search[0]
             title = search[0]
             url = search[1]
             duration = search[2]
             thumbnails = search[3]
             userid = sender.id
             titlegc = chat.title
             ctitle = await CHAT_TITLE(titlegc)
             thumb = await gen_thumb(thumbnail, title, userid, ctitle)
             format = "best[height<=?720][width<=?1280]"
             hm, ytlink = await ytdl(format, url)
             if hm == 0:
                 await botman.edit(f"`{ytlink}`")
             elif chat_id in QUEUE:
                 pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                 caption = f"💡 **Song Added To queue »** `#{pos}`\n\n**🏷 Title:** [{songname}]({url})\n**⏱ Duration:**  `{duration}`\n🎧 **On request:** {from_user}"
                 await botman.delete()
                 await event.client.send_file(chat_id, thumb, caption=caption)
             else:
                 try:
                     await call_py.join_group_call(
                         chat_id,
                         AudioPiped(
                             ytlink,
                         ),
                         stream_type=StreamType().pulse_stream,
                     )
                     add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                     caption = f"🏷 **Title:** [{songname}]({url})\n**⏱ Duration:** `{duration}`\n💡 **Status:** `Playing`\n  **On request:** {from_user}"
                     await botman.delete()
                     await event.client.send_file(chat_id, thumb, caption=caption)
                 except Exception as ep:
                     clear_queue(chat_id)
                     await botman.edit(f"`{ep}`")

     else:
         botman = await edit_or_reply(event, "📥 **Downloading**")
         dl = await replied.download_media()
         link = f"https://t.me/c/{chat.id}/{event.reply_to_msg_id}"
         if replied.audio:
             songname = "Telegram Music Player"
         elif replied. voice:
             songname = "Voice Note"
         if chat_id in QUEUE:
             pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
             caption = f"💡 **Song Added to queue »** `#{pos}`\n\n**🏷 Title:** [{songname}]({link})\n**👥 Chat ID:*  * `{chat_id}`\n🎧 **On request:** {from_user}"
             await event.client.send_file(chat_id, queue, caption=caption)
             await botman.delete()
         else:
             try:
                 await call_py.join_group_call(
                     chat_id,
                     AudioPiped(
                         etc.,
                     ),
                     stream_type=StreamType().pulse_stream,
                 )
                 add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                 caption = f"🏷 **Title:** [{songname}]({link})\n**👥 Chat ID:** `{chat_id}`\n💡 **Status:** `Playing Song`  \n🎧 **On request:** {from_user}"
                 await event.client.send_file(chat_id, fotoplay, caption=caption)
                 await botman.delete()
             except Exception as ep:
                 clear_queue(chat_id)
                 await botman.edit(f"`{ep}`")


 @alphonse_cmd(pattern="vplay(?:\s|$)([\s\S]*)")
 async def vc_vplay(event):
     title = event.pattern_match.group(1)
     replied = await event.get_reply_message()
     sender = await event.get_sender()
     userid = sender.id
     chat = await event.get_chat()
     titlegc = chat.title
     chat_id = event.chat_id
     from_user = vcmention(event.sender)
     if (
         replied
         and not replied.video
         and not replied.document
         and not title
         or not replied
         and not title
     ):
         return await edit_or_reply(event, "**Please Enter Video Title**")
     if replied and not replied.video and not replied.document:
         xnxx = await edit_or_reply(event, "`Searching...`")
         query = event.text.split(maxsplit=1)[1]
         search = ytsearch(query)
         RESOLUTION = 720
         hmmm = HighQualityVideo()
         if search == 0:
             await xnxx.edit(
                 "**Couldn't Find Video** Try Search With More Specific Title"
             )
         else:
             songname = search[0]
             title = search[0]
             url = search[1]
             duration = search[2]
             thumbnails = search[3]
             ctitle = await CHAT_TITLE(titlegc)
             thumb = await gen_thumb(thumbnail, title, userid, ctitle)
             format = "best[height<=?720][width<=?1280]"
             hm, ytlink = await ytdl(format, url)
             if hm == 0:
                 await xnxx.edit(f"`{ytlink}`")
             elif chat_id in QUEUE:
                 pos = add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUTION)
                 caption = f"💡 **Video Added To queue »** `#{pos}`\n\n**🏷 Title:** [{songname}]({url})\n**⏱ Duration:**  `{duration}`\n🎧 **On request:** {from_user}"
                 await xnxx.delete()
                 await event.client.send_file(chat_id, thumb, caption=caption)
             else:
                 try:
                     await call_py.join_group_call(
                         chat_id,
                         AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                         stream_type=StreamType().pulse_stream,
                     )
                     add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUTION)
                     await xnxx.edit(
                         f"**🏷 Title:** [{songname}]({url})\n**⏱ Duration:** `{duration}`\n💡 **Status:** `Video Playing`\n🎧  **On request:** {from_user}",
                         link_preview=False,
                     )
                 except Exception as ep:
                     clear_queue(chat_id)
                     await xnxx.edit(f"`{ep}`")

     elif replied:
         xnxx = await edit_or_reply(event, "📥 **Downloading**")
         dl = await replied.download_media()
         link = f"https://t.me/c/{chat.id}/{event.reply_to_msg_id}"
         if len(event.text.split()) < 2:
             RESOLUTION = 720
         else:
             pq = event.text.split(maxsplit=1)[1]
             RESOLUTION = int(pq)
         if replied.video or replied.document:
             songname = "Telegram Video Player"
         if chat_id in QUEUE:
             pos = add_to_queue(chat_id, songname, dl, link, "Video", RESOLUTION)
             caption = f"💡 **Video Added To Queue »** `#{pos}`\n\n**🏷 Title:** [{songname}]({link})\n**👥 Chat ID:*  * `{chat_id}`\n🎧 **On request:** {from_user}"
             await event.client.send_file(chat_id, queue, caption=caption)
             await xnxx.delete()
         else:
             if RESOLUTION == 360:
                 hmmm = LowQualityVideo()
             elif RESOLUTION == 480:
                 hmmm = MediumQualityVideo()
             elif RESOLUTION == 720:
                 hmmm = HighQualityVideo()
             try:
                 await call_py.join_group_call(
                     chat_id,
                     AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                     stream_type=StreamType().pulse_stream,
                 )
                 add_to_queue(chat_id, songname, dl, link, "Video", RESOLUTION)
                 caption = f"🏷 **Title:** [{songname}]({link})\n**👥 Chat ID:** `{chat_id}`\n💡 **Status:** `Video Playing`  \n🎧 **On request:** {from_user}"
                 await xnxx.delete()
                 await event.client.send_file(chat_id, fotoplay, caption=caption)
             except Exception as ep:
                 clear_queue(chat_id)
                 await xnxx.edit(f"`{ep}`")
     else:
         xnxx = await edit_or_reply(event, "`Searching...`")
         query = event.text.split(maxsplit=1)[1]
         search = ytsearch(query)
         RESOLUTION = 720
         hmmm = HighQualityVideo()
         if search == 0:
             await xnxx.edit("**Couldn't Find Video for Given Keyword**")
         else:
             songname = search[0]
             title = search[0]
             url = search[1]
             duration = search[2]
             thumbnails = search[3]
             ctitle = await CHAT_TITLE(titlegc)
             thumb = await gen_thumb(thumbnail, title, userid, ctitle)
             format = "best[height<=?720][width<=?1280]"
             hm, ytlink = await ytdl(format, url)
             if hm == 0:
                 await xnxx.edit(f"`{ytlink}`")
             elif chat_id in QUEUE:
                 pos = add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUTION)
                 caption = f"💡 **Video Added To queue »** `#{pos}`\n\n🏷 **Title:** [{songname}]({url})\n**⏱ Duration:**  `{duration}`\n🎧 **On request:** {from_user}"
                 await xnxx.delete()
                 await event.client.send_file(chat_id, thumb, caption=caption)
             else:
                 try:
                     await call_py.join_group_call(
                         chat_id,
                         AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                         stream_type=StreamType().pulse_stream,
                     )
                     add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUTION)
                     caption = f"🏷 **Title:** [{songname}]({url})\n**⏱ Duration:** `{duration}`\n💡 **Status:** `Video Playing`\  n🎧 **On request:** {from_user}"
                     await xnxx.delete()
                     await event.client.send_file(chat_id, thumb, caption=caption)
                 except Exception as ep:
                     clear_queue(chat_id)
                     await xnxx.edit(f"`{ep}`")


 @alphonse_cmd(pattern="end$")
 async def vc_end(event):
     chat_id = event.chat_id
     if chat_id in QUEUE:
         try:
             await call_py.leave_group_call(chat_id)
             clear_queue(chat_id)
             await edit_or_reply(event, "**Stop Streaming**")
         except Exception as e:
             await edit_delete(event, f"**ERROR:** `{e}`")
     else:
         await edit_delete(event, "**Not Playing Streaming**")


 @alphonse_cmd(pattern="skip(?:\s|$)([\s\S]*)")
 async def vc_skip(event):
     chat_id = event.chat_id
     if len(event.text.split()) < 2:
         op = await skip_current_song(chat_id)
         ifop == 0:
             await edit_delete(event, "**Not Playing Streaming**")
         elif op == 1:
             await edit_delete(event, "queue empty, left voice chat", 10)
         else:
             await edit_or_reply(
                 events,
                 f"**⏭ Skipping Song**\n**🎧 Now Playing** - [{op[0]}]({op[1]})",
                 link_preview=False,
             )
     else:
         skip = event.text.split(maxsplit=1)[1]
         DELQUE = "**Removing Following Songs From Queue:**"
         if chat_id in QUEUE:
             items = [int(x) for x in skip.split(" ") if x.isdigit()]
             items.sort(reverse=True)
             for x in items:
                 if x != 0:
                     hm = await skip_item(chat_id, x)
                     if hm != 0:
                         DELQUE = DELQUE + "\n" + f"**#{x}** - {hm}"
             await event.edit(DELQUE)


 @alphonse_cmd(pattern="pause$")
 async def vc_pause(event):
     chat_id = event.chat_id
     if chat_id in QUEUE:
         try:
             await call_py.pause_stream(chat_id)
             await edit_or_reply(event, "**Stream Paused**")
         except Exception as e:
             await edit_delete(event, f"**ERROR:** `{e}`")
     else:
         await edit_delete(event, "**Not Playing Streaming**")


 @alphonse_cmd(pattern="resume$")
 async def vc_resume(event):
     chat_id = event.chat_id
     if chat_id in QUEUE:
         try:
             await call_py.resume_stream(chat_id)
             await edit_or_reply(event, "**Stream Resume**")
         except Exception as e:
             await edit_or_reply(event, f"**ERROR:** `{e}`")
     else:
         await edit_delete(event, "**Not Playing Streaming**")


 @alphonse_cmd(pattern=r"volume(?: |$)(.*)")
 async def vc_volume(event):
     query = event.pattern_match.group(1)
     chat = await event.get_chat()
     admin = chat.admin_rights
     creator = chat.creator
     chat_id = event.chat_id

     if not admin and not creator:
         return await edit_delete(event, f"**Sorry {owner} Not Admin **", 30)

     if chat_id in QUEUE:
         try:
             await call_py.change_volume_call(chat_id, volume=int(query))
             await edit_or_reply(
                 event, f"**Successfully Changed Volume To** `{query}%`"
             )
         except Exception as e:
             await edit_delete(event, f"**ERROR:** `{e}`", 30)
     else:
         await edit_delete(event, "**Not Playing Streaming**")


 @alphonse_cmd(pattern="playlist$")
 async def vc_playlist(event):
     chat_id = event.chat_id
     if chat_id in QUEUE:
         chat_queue = get_queue(chat_id)
         if len(chat_queue) == 1:
             await edit_or_reply(
                 events,
                 f"**🎧 Playing:**\n• [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                 link_preview=False,
             )
         else:
             PLAYLIST = f"**🎧 Playing:**\n**• [{chat_queue[0][0]}]({chat_queue[0][2]})** | `{chat_queue[0][3  ]}` \n\n**• Playlists:**"
             l = len(chat_queue)
             for x in range(1, l):
                 hmm = chat_queue[x][0]
                 hmmm = chat_queue[x][2]
                 hmmmm = chat_queue[x][3]
                 PLAYLIST = PLAYLIST + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`"
             await edit_or_reply(event, PLAYLIST, link_preview=False)
     else:
         await edit_delete(event, "**Not Playing Streaming**")


 @call_py.on_stream_end()
 async def stream_end_handler(_, u: Update):
     chat_id = u.chat_id
     print(chat_id)
     await skip_current_song(chat_id)


 @call_py.on_closed_voice_chat()
 async def closedvc(_, chat_id: int):
     if chat_id in QUEUE:
         clear_queue(chat_id)


 @call_py.on_left()
 async def leftvc(_, chat_id: int):
     if chat_id in QUEUE:
         clear_queue(chat_id)


 @call_py.on_kicked()
 async def kickedvc(_, chat_id: int):
     if chat_id in QUEUE:
         clear_queue(chat_id)


 CMD_HELP.update(
     {
         "vcplugin": f"**Plugin : **`vcplugin`\
         \n\n • **Syntax :** `{cmd}play` <Song Title/YT Link>\
         \n • **Function : **To Play Songs in voice chat groups with your account\
         \n\n • **Syntax :** `{cmd}vplay` <Video Title/YT Link>\
         \n • **Function : **To Play Video in voice chat group with your account\
         \n\n • **Syntax :** `{cmd}end`\
         \n • **Function : **To stop the video/song currently playing in the voice chat group\
         \n\n • **Syntax :** `{cmd}skip`\
         \n • **Function : **To skip the currently playing video/song\
         \n\n • **Syntax :** `{cmd}pause`\
         \n • **Function : **To stop the currently playing video/song\
         \n\n • **Syntax :** `{cmd}resume`\
         \n • **Function : **To continue playing the currently playing video/song\
         \n\n • **Syntax :** `{cmd}volume` 1-200\
         \n • **Function : **To change volume (Requires admin rights)\
         \n\n • **Syntax :** `{cmd}playlist`\
         \n • **Function : **To display Song/Video playlist\
     "
     }
 )