# King - UserBot
# Copyright (C) 2020 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.
# PLease read the GNU Affero General Public License in

from telethon.errors import ChatSendInlineForbiddenError

from pyking import *
from pyking.misc._wrappers import eor
from pyking.misc._decorators import king_cmd

repomssg = (
    "• **KING-USERBOT** •\n\n",
    "• Repo - [Click Here](https://github.com/DoellBarr/King-Userbot)\n",
    "• Support - @KingUserbotSupport"
)


@king_cmd(pattern="repo$")
async def repify(e):
    try:
        q = await king_bot.inline_query(Var.BOT_USERNAME, "repo")
        await q[0].click(e.chat_id)
        if e.sender_id == king_bot.uid:
            await e.delete()
    except ChatSendInlineForbiddenError:
        await eor(e, repomssg)