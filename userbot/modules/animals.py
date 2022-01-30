import requests

 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP, bot
 from userbot.events import alphonse_cmd


 @bot.on(alphonse_cmd(outgoing=True, pattern="shibe$"))
 async def shibe(event):
     await event.edit("`Processing...`")
     response = requests.get("https://shibe.online/api/shibes").json()
     if not response:
         await event.edit("**Could not find Dog.**")
         return
     await event.client.send_message(entity=event.chat_id, file=response[0])
     await event.delete()


 @bot.on(alphonse_cmd(outgoing=True, pattern="cat$"))
 async def cats(event):
     await event.edit("`Processing...`")
     response = requests.get("https://shibe.online/api/cats").json()
     if not response:
         await event.edit("**Could not find cat.**")
         return
     await event.client.send_message(entity=event.chat_id, file=response[0])
     await event.delete()


 CMD_HELP.update(
     {
         "animals": f"**Plugin : **`animals`\
         \n\n • **Syntax :** `{cmd}cat`\
         \n • **Function : **To send random cat pictures.\
         \n\n • **Syntax :** `{cmd}shibe`\
         \n • **Function : **To send random pictures of Shiba breed dogs.\
     "
     }
 )