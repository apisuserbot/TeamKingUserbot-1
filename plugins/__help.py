# King - UserBot
# Copyright (C) 2020 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.

import logging

from support import *
from telethon.errors.rpcerrorlist import BotInlineDisabledError as dis
from telethon.errors.rpcerrorlist import BotMethodInvalidError as bmi
from telethon.errors.rpcerrorlist import BotResponseTimeoutError as rep

from pyking import *
from pyking.misc import *
from pyking.misc._decorators import king_cmd, eor, eod

from strings import get_string

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.WARNING)


@king_cmd(pattern="help ?(.*)")
async def king(event):
    plug = event.pattern_match.group(1)
    tgbot = Var.BOT_USERNAME
    if plug:
        try:
            if plug in HELP:
                output = f"**Plugin** - `{plug}`\n"
                for i in HELP[plug]:
                    output += i
                output += "\n©@KingUserbotChannel"
                await eor(event, output)
            elif plug in CMD_HELP:
                avail = f"Nama Plugin-{plug}\n\n✘ Perintah Tersedia -\n\n"
                avail += str(CMD_HELP[plug])
                await eor(event, avail)
            else:
                try:
                    x = f"Nama Plugin-{plug}\n\n✘ Perintah Tersedia -\n\n"
                    for d in LIST[plug]:
                        x += HNDLR + d
                        x += "\n"
                    await eor(event, x)
                except BaseException:
                    await eod(event, get_string("help_1").format(plug), time=5)
        except BaseException:
            await eor(event, "Terjadi sebuah error.")
    else:
        try:
            results = await king_bot.inline_query(tgbot, "kingd")
        except rep:
            return await eor(
                event,
                get_string("help_2").format(HNDLR),
            )
        except dis:
            return await eor(event, get_string("help_3"))
        except bmi:
            return await eor(
                event, get_string("help_4").format(tgbot),
            )
        await results[0].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
        await event.delete()