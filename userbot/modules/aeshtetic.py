from telethon import events

 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP, bot
 from userbot.events import alphonse_cmd

 PRINTABLE_ASCII = range(0x21, 0x7F)


 def aesthetics(string):
     for c in string:
         c = ord(c)
         if c in PRINTABLE_ASCII:
             c += 0xFF00 - 0x20
         elif c == ord(" "):
             c = 0x3000
         yield chr(c)


 @bot.on(alphonse_cmd(outgoing=True, pattern="ae(?: |$)(.*)"))
 async def _(event):
     if event.fwd_from:
         return
     text = event.pattern_match.group(1)
     text = "".join(aesthetics(text))
     await event.edit(text=text, parse_mode=None, link_preview=False)
     raise events.StopPropagation


 CMD_HELP.update(
     {
         "aeshtetic": f"**Plugin : **`aeshtetic`\
         \n\n • **Syntax :** `{cmd}ae <text>`\
         \n • **Function : **Change text font to aesthetic.\
     "
     }
 )