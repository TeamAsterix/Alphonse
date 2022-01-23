""" Userbot module for managing events.
 One of the main components of the userbot. """

import inspect
import re
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from os import remove
from pathlib import Path
from sys import exc_info
from time import gmtime, strftime
from traceback import format_exc

from telethon import events

from userbot import BOTLOG_CHATID, LOGS, LOGSPAMMER, bot

from . import CMD_HANDLER, SUDO_HANDLER, SUDO_LIST, SUDO_USERS


def is_chat_allowed(event_obj):
    try:
        from userbot.modules.sql_helper.blacklist_sql import get_blacklist

        for blacklisted in get_blacklist():  # type: ignore
            if str(event_obj.chat_id) == blacklisted.chat_id:
                return False
    except Exception:
        pass

    return True


# Thanks for https://github.com/ULTRA-OP/ULTRA-X/
def admin_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    global SUDO_USERS
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    # get the pattern from the decorator
    if pattern is not None:
        if pattern.startswith(r"\#"):
            # special fix for snip.py
            args["pattern"] = re.compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = re.compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                CMD_LIST = {}[file_test].append(cmd)
            except BaseException:
                CMD_LIST = {}.update({file_test: [cmd]})
        else:
            if len(CMD_HANDLER) == 2:
                catreg = "^" + CMD_HANDLER
                reg = CMD_HANDLER[1]
            elif len(CMD_HANDLER) == 1:
                catreg = "^\\" + CMD_HANDLER
                reg = CMD_HANDLER
            args["pattern"] = re.compile(catreg + pattern)
            if command is not None:
                cmd = reg + command
            else:
                cmd = (
                    (reg + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
            try:
                CMD_LIST = {}[file_test].append(cmd)
            except BaseException:
                CMD_LIST = {}.update({file_test: [cmd]})

    args["outgoing"] = True
    # should this command be available for other users?
    if allow_sudo:
        args["from_users"] = list(SUDO_USERS)
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]

    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    # add blacklist chats, UB should not respond in these chats
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]


# Thanks for https://github.com/ULTRA-OP/ULTRA-X/
def sudo_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    # get the pattern from the decorator
    if pattern is not None:
        if pattern.startswith(r"\#"):
            # special fix for snip.py
            args["pattern"] = re.compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = re.compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                SUDO_LIST[file_test].append(cmd)
            except BaseException:
                SUDO_LIST.update({file_test: [cmd]})
        else:
            if len(SUDO_HANDLER) == 2:
                mafiareg = "^" + SUDO_HANDLER
                reg = SUDO_HANDLER[1]
            elif len(SUDO_HANDLER) == 1:
                mafiareg = "^\\" + SUDO_HANDLER
                reg = SUDO_HANDLER
            args["pattern"] = re.compile(mafiareg + pattern)
            if command is not None:
                cmd = reg + command
            else:
                cmd = (
                    (reg + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
            try:
                SUDO_LIST[file_test].append(cmd)
            except BaseException:
                SUDO_LIST.update({file_test: [cmd]})
    args["outgoing"] = True
    # should this command be available for other users?
    if allow_sudo:
        args["from_users"] = list(SUDO_USERS)
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]
    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    # check if the plugin should listen for outgoing 'messages'
    return events.NewMessage(**args)


def register(**args):
    """Register a new event."""
    pattern = args.get("pattern", None)
    disable_edited = args.get("disable_edited", False)
    ignore_unsafe = args.get("ignore_unsafe", False)
    unsafe_pattern = r"^[^/!#@\$A-Za-z]"
    disable_errors = args.get("disable_errors", False)

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    if "disable_edited" in args:
        del args["disable_edited"]

    if "ignore_unsafe" in args:
        del args["ignore_unsafe"]

    if "disable_errors" in args:
        del args["disable_errors"]

    if pattern and not ignore_unsafe:
        args["pattern"] = pattern.replace("^.", unsafe_pattern, 1)

    def decorator(func):
        async def wrapper(check):
            if check.edit_date and check.is_channel and not check.is_group:
                # Messages sent in channels can be edited by other users.
                # Ignore edits that take place in channels.
                return

            if not is_chat_allowed(check):
                return

            if check.via_bot_id and check.out:
                return

            try:
                await func(check)
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException as e:
                # Check if we have to disable error logging.
                if not disable_errors:
                    LOGS.exception(e)  # Log the error in console

                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    link = "[Issues](https://github.com/TeamAlphonse/Alphonse/issues)"
                    text = (
                        "**ALPHONSE ERROR REPORT**\n"
                        "If you want to, you can report it"
                        f"- just upload this file to {link}.\n"
                        "I won't log anything except the fact of error and date\n"
                    )

                    command = 'git log --pretty=format:"%an: %s" -10'

                    process = await asyncsubshell(
                        command, stdout=asyncsub.PIPE, stderr=asyncsub.PIPE
                    )
                    stdout, stderr = await process.communicate()
                    ftext = (
                        "\nDisclaimer:\nThis file uploaded ONLY here, we "
                        "logged only fact of error and date, we respect your "
                        "privacy, you may not report this error if you've any "
                        "confidential data here, no one will see your data if "
                        "you choose not to do so.\n\n"
                        "--------BEGIN USERBOT TRACEBACK LOG--------"
                        f"\nDate: {date}\nChat ID: {check.chat_id}"
                        f"\nSender ID: {check.sender_id}\n\nEvent Trigger:\n"
                        f"{check.text}\n\nTraceback info:\n{format_exc()}"
                        f"\n\nError text:\n{exc_info()[1]}"
                        "\n\n--------END USERBOT TRACEBACK LOG--------"
                        "\n\n\nLast 10 commits:\n"
                        f"{stdout.decode().strip()}{stderr.decode().strip()}"
                    )

                    with open("error.log", "w+") as file:
                        file.write(ftext)

                    if LOGSPAMMER:
                        await check.client.send_file(
                            BOTLOG_CHATID,
                            "error.log",
                            caption=text,
                        )
                    else:
                        await check.client.send_file(
                            check.chat_id,
                            "error.log",
                            caption=text,
                        )

                    remove("error.log")

        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator
