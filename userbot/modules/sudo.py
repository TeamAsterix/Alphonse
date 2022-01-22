import heroku3, re

from userbot import CMD_HELP, HEROKU_API_KEY, HEROKU_APP_NAME, SUDO_USERS as sudos, bot
from userbot.events import register


Heroku = heroku3.from_key(HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"


@register(outgoing=True, pattern=r"^\.listsudo$")
async def sudo(sudo_users):
    sduo = "True" if sudos else "False"
    user = sudos

    if sduo == "True":
        await sudo_users.edit(
            f"**Sudo Mode** : `Enabled`\n\n **Sudo users** : `{user}`"
        )
    else:
        await sudo_users.edit(f"**Sudo Mode** : `Disabled`")


@register(outgoing=True, pattern=r"^\.addsudo$")
async def addsudo(event):
    await event.edit("Adding User as Sudo")
    app = Heroku.app(HEROKU_APP_NAME)
    var = app.config()

    if event.is_reply:
        id = (await event.get_reply_message()).sender_id
        name = (await bot.get_entity(id)).first_name

        await event.edit(
            f"✅ Successfully Added **{name}** as a sudo user. \n Please wait for restarting bot."
        )
        var["SUDO_USERS"] = id

    else:
        await event.edit("Please Reply to a message")


@register(outgoing=True, pattern=r"^\.remsudo$")
async def remsudo(event):
    await event.edit("processing...")
    app = Heroku.app(HEROKU_APP_NAME)
    var = app.config()

    if event.is_reply:
        id = (await event.get_reply_message()).sender_id
        name = (await bot.get_entity(id)).first_name
        in_sudo = re.search(str(id), str(sudos))

        if in_sudo:
            i = ""
            amazing = sudos.split(" ")
            amazing.remove(str(id))
            i += str(amazing)
            x = i.replace("[", "")
            xx = x.replace("]", "")
            xxx = xx.replace(",", "")
            done = xxx.replace("'", "")
            var["SUDO_USERS"] = done
            await event.edit(
                f"Successfully Removed **{name}** is sudo user. \n please wait for reastart me."
            )

        else:
            await event.edit(f"{name} is not in a sudo user.")
    else:
        await event.edit("please reply to a message.")
