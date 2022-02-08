

from requests import get
from alphonsebot import HELP, ALPHONSE_LANG, WEATHER
from alphonseecem.core import edit, extract_args, get_translation, alphonseify

# ===== CONSTANT =====
if WEATHER:
    DEFCITY = WEATHER
else:
    DEFCITY = None
# ====================


@alphonseify(pattern='^.(havadurumu|w(eathe|tt)r)')
def havadurumu(message):
    args = extract_args(message)

    if len(args) < 1:
        CITY = DEFCITY
        if not CITY:
            edit(message, f'`{get_translation("weatherErrorCity")}`')
            return
    else:
        CITY = args

    if ',' in CITY:
        CITY = CITY[: CITY.find(',')].strip()

    try:
        req = get(
            f'http://wttr.in/{CITY}?mqT0',
            headers={'User-Agent': 'curl/7.66.0', 'Accept-Language': ALPHONSE_LANG},
        )
        data = req.text
        if '===' in data:
            raise Exception
        data = data.replace('`', '‛')
        edit(message, f'`{data}`')
    except Exception:
        edit(message, f'`{get_translation("weatherErrorServer")}`')


HELP.update({'weather': get_translation('infoWeather')})
