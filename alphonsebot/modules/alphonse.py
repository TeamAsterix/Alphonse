

from collections import OrderedDict

from alphonsebot import HELP
from alphonseecem.core import edit, extract_args, get_translation, reply, alphonseify


@alphonseify(pattern='^.alphonse')
def alphonse(message):
    alphonse = extract_args(message).lower()
    cmds = OrderedDict(sorted(HELP.items()))
    if len(alphonse) > 0:
        if alphonse in cmds:
            edit(message, str(cmds[alphonse]))
        else:
            edit(message, f'**{get_translation("alphonseUsage")}**')
    else:
        edit(message, get_translation('alphonseUsage2', ['**', '`']))
        metin = f'{get_translation("alphonseShowLoadedModules", ["**", "`", len(cmds)])}\n'
        for item in cmds:
            metin += f'• `{item}`\n'
        reply(message, metin)
