

import math
import time

from telethon.errors.rpcerrorlist import MessageNotModifiedError

from .exceptions import CancelProcess
from .tools import humanbytes, time_formatter


async def progress(current, total, event, start, prog_type, is_cancelled=False):
    now = time.time()
    diff = now - start
    if is_cancelled is True:
        raise CancelProcess

    if round(diff % 15.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff)
        eta = round((total - current) / speed)
        if "upload" in prog_type.lower():
            status = "Uploading"
        elif "download" in prog_type.lower():
            status = "Downloading"
        else:
            status = "Status"
        progress_str = "**{}:** `[{}{}]` **{}%**".format(
            status,
            "".join("●" for _ in range(math.floor(percentage / 10))),
            "".join("○" for _ in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        tmp = (
            f"{progress_str}\n"
            f"{humanbytes(current)} of {humanbytes(total)}"
            f" @ {humanbytes(speed)}\n"
            f"**ETA:** {time_formatter(eta)}\n"
            f"**Duration:** {time_formatter(elapsed_time)}"
        )
        try:
            await event.edit(f"**{prog_type}**\n\n{tmp}")
        except MessageNotModifiedError:
            pass
