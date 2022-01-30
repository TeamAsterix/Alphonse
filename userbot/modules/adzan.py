# ported from uniborg
 # https://github.com/muhammedfurkan/UniBorg/blob/master/stdplugins/ezanvaakti.py

 import json

 import requests

 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP
 from userbot.modules.sql_helper.globals import gvarstatus
 from userbot.utils import edit_delete, edit_or_reply, alphonse_cmd


 @alphonse_cmd(pattern="adhan(?:\s|$)([\s\S]*)")
 async def get_adzan(adhan):
     "Shows you the Islamic prayer times of the given city name"
     input_str = adzan.pattern_match.group(1)
     LOCATION = gvarstatus("WEATHER_DEFCITY") or "Jakarta" if not input_str else input_str
     url = f"http://muslimsalat.com/{LOCATION}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
     request = requests.get(url)
     if request.status_code != 200:
         return await edit_delete(
             adhan, f"**Cannot Find City** `{LOCATION}`", 120
         )
     result = json.loads(request.text)
     catresult = f"<b>Today's Prayer Schedule:</b>\
             \n<b>📆 Date </b><code>{result['items'][0]['date_for']}</code>\
             \n<b>📍 City</b> <code>{result['query']}</code> |  <code>{result['country']}</code>\
             \n\n<b>Published : </b><code>{result['items'][0]['shurooq']}</code>\
             \n<b>Dawn : </b><code>{result['items'][0]['fajr']}</code>\
             \n<b>Dawn : </b><code>{result['items'][0]['dhuhr']}</code>\
             \n<b>Asr : </b><code>{result['items'][0]['asr']}</code>\
             \n<b>Maghrib : </b><code>{result['items'][0]['Maghrib']}</code>\
             \n<b>Isha : </b><code>{result['items'][0]['isha']}</code>\
     "
     await edit_or_reply(adhan, catresult, "html")


 CMD_HELP.update(
     {
         "adhan": f"**Plugin : **`adzan`\
         \n\n • **Syntax :** `{cmd}adhan` <city name>\
         \n • **Function : **Shows the prayer times of the given city.\
     "
     }
 )