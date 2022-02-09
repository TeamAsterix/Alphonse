

from os import remove

from alphonsebot import LOG_ID, app

from .send import send, send_doc


def send_log(text, fix_markdown=False):
    send(app, LOG_ID or 'me', text, fix_markdown=fix_markdown)


def send_log_doc(doc, caption='', fix_markdown=False, remove_file=False):
    send_doc(app, LOG_ID or 'me', doc, caption=caption, fix_markdown=fix_markdown)
    if remove_file:
        remove(doc)
