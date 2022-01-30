import random
 import time
 from datetime import datetime

 from speedtest import Speedtest

 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP, StartTime, bot
 from userbot.events import register
 from userbot.utils import edit_or_reply, humanbytes, alphonse_cmd

 absent = [
     "**Coming bang** ",
     "**Present Sis** ",
     "**Come please** ",
     "**Present handsome** ",
     "**Coming bro** ",
     "**Come here, sorry for being late** ",
 ]


 async def get_readable_time(seconds: int) -> str:
     count = 0
     up_time = ""
     time_list = []
     time_suffix_list = ["s", "m", "Hours", "Days"]

     while count < 4:
         count += 1
         remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
         if seconds == 0 and remainder == 0:
             break
         time_list.append(int(result))
         seconds = int(remainder)

     for x in range(len(time_list)):
         time_list[x] = str(time_list[x]) + time_suffix_list[x]
     if len(time_list) == 4:
         up_time += time_list.pop() + ","

     time_list.reverse()
     up_time += ":".join(time_list)

     return up_time


 @alphonse_cmd(pattern="ping$")
 async def _(ping):
     """For .ping command, ping the userbot from any chat."""
     uptime = await get_readable_time((time.time() - StartTime))
     start = datetime.now()
     xx = await edit_or_reply(ping, "**✣**")
     await xx.edit("**✣✣**")
     await xx.edit("**✣✣✣**")
     await xx.edit("**✣✣✣✣**")
     end = datetime.now()
     duration = (end - start).microseconds / 1000
     user = await bot.get_me()
     await xx.edit(
         f"**PONG!!🏓**\n"
         f"✣ **Pinger** - `%sms`\n"
         f"✣ **Uptime -** `{uptime}` \n"
         f"**✦҈͜͡Owner :** [{user.first_name}](tg://user?id={user.id})" % (duration)
     )


 @alphonse_cmd(pattern=r"xping$")
 async def _(ping):
     """For .ping command, ping the userbot from any chat."""
     uptime = await get_readable_time((time.time() - StartTime))
     start = datetime.now()
     xping = await edit_or_reply(ping, "`Pinging....`")
     end = datetime.now()
     duration = (end - start).microseconds / 1000
     await xping.edit(
         f"**PONG!! **\n**Pinger** : %sms\n**Bot Uptime** : {uptime}🕛" % (duration)
     )


 @alphonse_cmd(pattern=r"lping$")
 async def _(ping):
     """For .ping command, ping the userbot from any chat."""
     uptime = await get_readable_time((time.time() - StartTime))
     start = datetime.now()
     lping = await edit_or_reply(ping, "**★ PING **")
     await lping.edit("**★★ PING **")
     await lping.edit("**★★★ PING **")
     await lping.edit("**★★★★ PING **")
     await lping.edit("**✦҈͜͡➳ PONG!**")
     end = datetime.now()
     duration = (end - start).microseconds / 1000
     user = await bot.get_me()
     await lping.edit(
         f"❃ **Ping !!** "
         f"`%sms` \n"
         f"❃ **Uptime -** "
         f"`{uptime}` \n"
         f"**✦҈͜͡➳ Master :** [{user.first_name}](tg://user?id={user.id})" % (duration)
     )


 @alphonse_cmd(pattern=r"chips$")
 async def _(pong):
     await get_readable_time((time.time() - StartTime))
     start = datetime.now()
     kopong = await edit_or_reply(pong, "**『⍟C O C K』**")
     await kopong.edit("**◆◈C A M P◈◆**")
     await kopong.edit("**S O L V E**")
     await kopong.edit("**R E A D Y**")
     end = datetime.now()
     duration = (end - start).microseconds / 1000
     user = await bot.get_me()
     await kopong.edit(
         f"**✲ ** "
         f"\n `%sms` \n"
         f"**✲ ** "
         f"\n [{user.first_name}](tg://user?id={user.id})』 \n" % (duration)
     )


 # .chip & kping Coded by Koala


 @alphonse_cmd(pattern=r"kping$")
 async def _(pong):
     uptime = await get_readable_time((time.time() - StartTime))
     start = datetime.now()
     kping = await edit_or_reply(pong, "8✊===D")
     await kping.edit("8=✊==D")
     await kping.edit("8==✊=D")
     await kping.edit("8===✊D")
     await kping.edit("8==✊=D")
     await kping.edit("8=✊==D")
     await kping.edit("8✊===D")
     await kping.edit("8=✊==D")
     await kping.edit("8==✊=D")
     await kping.edit("8===✊D")
     await kping.edit("8==✊=D")
     await kping.edit("8=✊==D")
     await kping.edit("8✊===D")
     await kping.edit("8=✊==D")
     await kping.edit("8==✊=D")
     await kping.edit("8===✊D")
     await kping.edit("8===✊D💦")
     await kping.edit("8====D💦💦")
     await kping.edit("** CROOTTTT PINGGGG!**")
     end = datetime.now()
     duration = (end - start).microseconds / 1000
     await kping.edit(
         f"**FUCK!! **\n**KAMPANG** : %sms\n**Bot Uptime** : {uptime}🕛" % (duration)
     )


 @alphonse_cmd(pattern="speedtest$")
 async def _(speed):
     """For .speedtest command, use SpeedTest to check server speeds."""
     xxnx = await edit_or_reply(speed, "`Running speed test...`")
     test = Speedtest()
     test.get_best_server()
     test.download()
     test.upload()
     test.results.share()
     result = test.results.dict()
     msg = (
         f"**Started at {result['timestamp']}**\n\n"
         "**Client**\n"
         f"**ISP :** `{result['client']['isp']}`\n"
         f"**Country :** `{result['client']['country']}`\n\n"
         "**Servers**\n"
         f"**Name :** `{result['server']['name']}`\n"
         f"**Country :** `{result['server']['country']}`\n"
         f"**Sponsor :** `{result['server']['sponsor']}`\n\n"
         f"**Ping :** `{result['ping']}`\n"
         f"**Upload :** `{humanbytes(result['upload'])}/s`\n"
         f"**Download :** `{humanbytes(result['download'])}/s`"
     )
     await xxnx.delete()
     await speed.client.send_file(
         speed.chat_id,
         result["share"],
         caption=msg,
         force_document=False,
     )


 @alphonse_cmd(pattern="pong$")
 async def _(pong):
     """For .ping command, ping the userbot from any chat."""
     start = datetime.now()
     xx = await edit_or_reply(pong, "`Sepong.....🏓`")
     end = datetime.now()
     duration = (end - start).microseconds / 9000
     await xx.edit("🏓 **Ping!**\n`%sms`" % (duration))


 # If you are absent, you don't have to delete it, you idiot
 @register(pattern=r"^\.absent$", sudo=True)
 async def risman(handsome):
     await handsome.reply(random.choice(absent))


 # DON'T REMOVE GOBLOK YOU COPY ONLY JUST ADDED
 # REMOVED I AM GBAN YES I SIGNED YOU TELENYA ACCOUNT


 CMD_HELP.update(
     {
         "ping": f"**Plugin : **`ping`\
         \n\n • **Syntax :** `{cmd}ping` ;  `{cmd}lping` ;  `{cmd}xping` ;  `{cmd}kping`\
         \n • **Function : **To show userbot ping.\
         \n\n • **Syntax :** `{cmd}pong`\
         \n • **Function : **Same as ping command\
     "
     }
 )


 CMD_HELP.update(
     {
         "speedtest": f"**Plugin : **`speedtest`\
         \n\n • **Syntax :** `{cmd}speedtest`\
         \n • **Function : **To test the speed of the userbot server.\
     "
     }
 )