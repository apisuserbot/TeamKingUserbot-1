# King - UserBot
# Copyright (C) 2020 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.
# PLease read the GNU Affero General Public License in

from telethon import custom, events
from telethon.utils import get_display_name

from pyking import *
from pyking.__main__ import asst


@king_bot.on(
    events.NewMessage(incoming=True, func=lambda e: (e.mentioned))
)
async def all_messages_catcher(e):
    if udB.get("TAG_LOG") is not None:
        tag_logg = int(udB.get("TAG_LOG"))
        x = await king_bot.get_entity(e.sender_id)
        if x.bot or x.verified:
            return
        y = await king_bot.get_entity(e.chat_id)
        if y.username:
            yy = f"[{get_display_name(y)}](https://t.me/{y.username})"
        else:
            yy = f"[{get_display_name(y)}](https://t.me/c/{y.id}/{e.id})"
        xx = f"[{get_display_name(x)}](tg://user?id={x.id})"
        msg = f"https://t.me/c/{y.id}/{e.id}"
        if e.text:
            cap = f"{xx} men-tag kamu di {yy}\n\n```{e.text}```"
        else:
            cap = f"{xx} men-tag kamu di {yy}"

        btx = "📨 Lihat Pesan"

        try:
            if e.text:
                cap = f"{xx} men-tag kamu di {yy}\n\n```{e.text}```"
            else:
                cap = f"{xx} men-tag kamu di {yy}\n\n"
            await asst.send_message(
                tag_logg,
                cap,
                link_preview=False,
                buttons=[[custom.Button.url(btx, msg)]],
            )
        except BaseException:
            if e.text:
                cap = f"{xx} men-tag kamu di {yy}\n\n```{e.text}```"
            else:
                cap = f"{xx} men-tag kamu di {yy}\n\n"
            try:
                await king_bot.send_message(tag_logg, cap, link_preview=False)
            except BaseException:
                pass
    else:
        return