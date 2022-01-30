import sys
 from os import environ, execle, remove

 from git import Repo
 from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP, HEROKU_API_KEY, HEROKU_APP_NAME, UPSTREAM_REPO_URL
 from userbot.utils import edit_delete, edit_or_reply, alphonse_cmd


 async def gen_chlog(repo, diff):
     d_form = "%d/%m/%y"
     return "".join(
         f"• [{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n"
         for c in repo.iter_commits(diff)
     )


 async def print_changelogs(xx, ac_br, changelog):
     changelog_str = (
         f"**✥ Update Available For [{ac_br}] :\n\n✥ Update:**\n`{changelog}`"
     )
     if len(changelog_str) > 4096:
         await edit_or_reply(xx, "**Changelog too large, sent as file.**")
         with open("output.txt", "w+") as file:
             file.write(changelog_str)
         await xx.client.send_file(xx.chat_id, "output.txt")
         remove("output.txt")
     else:
         await xx.client.send_message(xx.chat_id, changelog_str)
     return True


 async def deploy(xx, repo, ups_rem, ac_br, txt):
  if HEROKU_API_KEY is None:
   return await edit_delete(
       xx, "**[HEROKU]: Please Add Variable** `HEROKU_API_KEY`"
   )
  import heroku3

  heroku = heroku3.from_key(HEROKU_API_KEY)
  heroku_app = None
  heroku_applications = heroku.apps()
  if HEROKU_APP_NAME is None:
      await edit_or_reply(
          xx,
          "**[HEROKU]: Please Add Variable** `HEROKU_APP_NAME` "
          " **to deploy the latest changes from Userbot.**",
      )
      repo.__del__()
      return
  for app in heroku_applications:
      if app.name == HEROKU_APP_NAME:
          heroku_app = app
          break
  if heroku_app is None:
      await edit_or_reply(
          xx,
          f"{txt}\n"
          "**Invalid Heroku credentials for deploying Alphonse dyno.**",
      )
      return repo.__del__()
  try:
      from userbot.modules.sql_helper.globals import addgvar, delgvar

      delgvar("restartstatus")
      addgvar("restartstatus", f"{xx.chat_id}\n{xx.id}")
  except AttributeError:
      pass
  ups_rem.fetch(ac_br)
  repo.git.reset("--hard", "FETCH_HEAD")
  heroku_git_url = heroku_app.git_url.replace(
      "https://", "https://api:" + HEROKU_API_KEY + "@"
  )
  if "heroku" in repo.remotes:
      remote = repo.remote("heroku")
      remote.set_url(heroku_git_url)
  else:
      remote = repo.create_remote("heroku", heroku_git_url)
  try:
      remote.push(refspec="HEAD:refs/heads/master", force=True)
  except Exception as error:
      await edit_or_reply(xx, f"{txt}\n**Error Occurred In Log:**\n`{error}`")
      return repo.__del__()
  build = heroku_app.builds(order_by="created_at", sort="desc")[0]
  if build.status == "failed":
      await edit_delete(
          xx, "**Build Failed!** Aborted due to some errors.`"
      )
  await edit_or_reply(
      xx, "`Alphonse Successfully Deployed! Userbot can be reused.`"
  )


 async def update(xx, repo, ups_rem, ac_br):
     try:
         ups_rem.pull(ac_br)
     except GitCommandError:
         repo.git.reset("--hard", "FETCH_HEAD")
     await edit_or_reply(
         xx, "`Alphonse Updated Successfully! Userbot can be used again.`"
     )

     try:
         from userbot.modules.sql_helper.globals import addgvar, delgvar

         delgvar("restartstatus")
         addgvar("restartstatus", f"{xx.chat_id}\n{xx.id}")
     except AttributeError:
         pass

     # Spin a new instance of bot
     args = [sys.executable, "-m", "userbot"]
     execle(sys.executable, *args, environ)


 @alphonse_cmd(pattern="update( now| deploy|$)")
 async def upstream(event):
  "For .update command, check if the bot is up to date, update if specified"
  xx = await edit_or_reply(event, "`Checking for Updates, Wait a moment...`")
  conf = event.pattern_match.group(1).strip()
  off_repo = UPSTREAM_REPO_URL
  force_update = False
  try:
   txt = ("**Update Could Not Continue Because " +
          "Multiple ERRORs**\n\n**LOGTRACE:**\n")
   repo = repo()
  except NoSuchPathError as error:
      await xx.edit(f"{txt}\n**Directory** `{error}` **Cannot Be Found.**")
      return repo.__del__()
  except GitCommandError as error:
      await xx.edit(f"{txt}\n**Initial failure!** `{error}`")
      return repo.__del__()
  except InvalidGitRepositoryError as error:
      if conf is None:
          return await xx.edit(
              f"**Unfortunately, Directory {error} Doesn't Appear From Repo."
              "\nBut We Can Force Update Userbot Using** `.update deploy`"
          )
      repo = Repo.init()
      origin = repo.create_remote("upstream", off_repo)
      origin.fetch()
      force_update = True
      repo.create_head("master", origin.refs.master)
      repo.heads.master.set_tracking_branch(origin.refs.master)
      repo.heads.master.checkout(True)

  ac_br = repo.active_branch.name
  try:
      repo.create_remote("upstream", off_repo)
  except BaseException:
      pass

  ups_rem = repo.remote("upstream")
  ups_rem.fetch(ac_br)

  changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
  if conf == "deploy":
      await xx.edit("`[HEROKU]: Alphonse Deploy Update is in Progress...`")
      await deploy(xx, repo, ups_rem, ac_br, txt)
      return

  if changelog == "" and not force_update:
      await edit_delete(xx, "**✥ Alphonse is the latest version**")
      return repo.__del__()

  if conf == "" and not force_update:
      await print_changelogs(xx, ac_br, changelog)
      await xx.delete()
      return await event.respond(
          "**Type** `.update deploy` **to Update Userbot.**"
      )

  if force_update:
      await xx.edit("**Forced Sync To Latest Userbot Code, Please Wait...**")

  if conf == "now":
      for commit in changelog.splitlines():
          if (
              commit.startswith("- [NQ]")
              and HEROKU_APP_NAME is not None
              and HEROKU_API_KEY is not None
          ):
              return await xx.edit(
                  "**Quick update has been disabled for this update; "
                  "Use** `.update deploy` **instead.**"
              )
      await xx.edit("**Performing a quick update, please wait...**")
      await update(xx, repo, ups_rem, ac_br)

  return


 CMD_HELP.update(
     {
         "update": f"**Plugin : **`update`\
         \n\n • **Syntax :** `{cmd}update`\
         \n • **Function : **To View Latest Alphonse Updates.\
         \n\n • **Syntax :** `{cmd}update deploy`\
         \n • **Function : **To Update Latest Features From Alphonse.\
     "
     }
 )