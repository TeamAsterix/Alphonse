

from math import floor
from subprocess import Popen

from PIL import Image

from .misc import get_download_dir


def sticker_resize(photo):
    image = Image.open(photo)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = floor(size1new)
        size2new = floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        maxsize = (512, 512)
        image.thumbnail(maxsize)

    temp = f'{get_download_dir()}/temp.png'
    image.save(temp, 'PNG')
    return temp


def video_convert(video):
    process = Popen(
        [
            'ffmpeg',
            '-i',
            f'{video}',
            '-vf',
            'scale=512:512:force_original_aspect_ratio=decrease',
            '-c:v',
            'libvpx-vp9',
            '-crf',
            '30',
            '-b:v',
            '500k',
            '-pix_fmt',
            'yuv420p',
            '-t',
            '2.9',
            '-an',
            '-y',
            f'{get_download_dir()}/temp.webm',
        ]
    )
    _ = process.communicate()
    output = f'{get_download_dir()}/temp.webm'
    return output
