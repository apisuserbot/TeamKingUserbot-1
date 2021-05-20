# KingUserbot
# Copyright (C) 2021 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.

import functools
from telethon import events
from .. import *
from .. import king_bot
from ..utils import *
from ._decorators import sed
from telethon.tl.types import InputWebDocument
from telethon.utils import get_display_name

OWNER_NAME = king_bot.me.first_name
OWNER_ID = king_bot.me.id
KING_PIC = "https://telegra.ph/file/1496ffecb9d6422e2ffd0.jpg"

MSG = f"""
**King Userbot**
➖➖➖➖➖➖➖➖➖➖
**Owner**: [{get_display_name(king_bot.me)}](tg://user?id={OWNER_ID}
**Support**: @KingUserbotSupport
➖➖➖➖➖➖➖➖➖➖
"""


# Handler Decorator untuk Assisten

def in_owner():
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(event):
            if event.sender_id in sed:
                try:
                    await function(event)
                except BaseException as be:
                    pass
            else:
                try:
                    builder = event.builder
                    sur = builder.article(
                        title="King Userbot",
                        url="https://t.me/KingUserbotSupport",
                        description="(c) KingUserbot",
                        text=MSG,
                        thumb=InputWebDocument(KING_PIC, 0, "image/jpeg", []),
                        buttons=[
                            [
                                Button.url(
                                    "Repository",
                                    url="https://github.com/DoellBarr/King-Userbot"
                                ),
                                Button.url(
                                    "Support",
                                    url="https://t.me/KingUserbotSupport"
                                ),
                            ]
                        ],
                    )
                    await event.answer(
                        [sur],
                        switch_pm=f"🤖: Asisten dari {OWNER_NAME}",
                        switch_pm_param="start",
                    )
                except BaseException as bexc:
                    pass

        return wrapper

    return decorator


def asst_cmd(dec):
    def ult(func):
        pattern = "^/" + dec
        king_bot.asst.add_event_handler(
            func, events.NewMessage(incoming=True, pattern=pattern)
        )

    return ult


def callback(sod):
    def king(func):
        data = sod
        king_bot.asst.add_event_handler(
            func, events.callbackquery.CallbackQuery(data=data)
        )

    return king


def inline():
    def kings(func):
        king_bot.asst.add_event_handler(func, events.InlineQuery)

    return kings


def in_pattern(pat):
    def don(func):
        pattern = pat
        king_bot.asst.add_event_handler(func, events.InlineQuery(pattern=pattern))

    return don


def owner():
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(event):
            if event.sender_id in sed:
                await function(event)
            else:
                try:
                    await event.answer(f"Ini adalah botnya {OWNER_NAME}!!", alert=True)
                except BaseException:
                    pass

        return wrapper

    return decorator
