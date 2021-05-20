# King - UserBot
# Copyright (C) 2020 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.
from pyking import king_bot
from pyking.functions import *
from pyking.functions.all import *

try:
    import glitch_me
except ModuleNotFoundError:
    os.system(
        "git clone https://github.com/1Danish-00/glitch_me.git && pip install -e ./glitch_me "
    )

start_time = time.time()
king_version = "v1.0.0"
OWNER_NAME = king_bot.me.first_name
OWNER_ID = king_bot.me.id


def grt(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["detik", "memot", "jam", "hari"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


KANGING_STR = [
    "Mencuri stiker...",
    "Curi aja cepet",
    "Cepet ambil tolol",
    "Woi ambil stikernya ajg",
    "Misi numpang curi",
]


