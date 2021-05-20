# King - UserBot
# Copyright (C) 2020 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.
# PLease read the GNU Affero General Public License in

import re

from telethon import Button
from telethon.errors.rpcerrorlist import BotInlineDisabledError as dis
from telethon.errors.rpcerrorlist import BotResponseTimeoutError as rep
from telethon.errors.rpcerrorlist import MessageNotModifiedError as np
from telethon.tl.functions.users import GetFullUserRequest as gu
from telethon.tl.types import UserStatusEmpty as mt
from telethon.tl.types import UserStatusLastMonth as lm
from telethon.tl.types import UserStatusLastWeek as lw
from telethon.tl.types import UserStatusOffline as off
from telethon.tl.types import UserStatusOnline as on
from telethon.tl.types import UserStatusRecently as rec

from pyking import *
from pyking.misc._assistant import in_pattern, callback
from pyking.misc._wrappers import eor, eod
from pyking.misc._decorators import king_cmd

reasons = {}
userss = []

@king_cmd(pattern="wspr ?(.*)")
async def _(e):
    if e.reply_to_msg_id:
        okk = (await e.get_reply_message()).sender_id
        try:
            zyx = await king_bot(gu(id=okk))
            put = zyx.user.username
        except ValueError as ve:
            return await eor(e, str(ve))
        except AttributeError:
            return await eor(e, "Tidak ada username dari user yang kamu balas")
    else:
        put = e.pattern_match.group(1)
    if put:
        try:
            results = await king_bot.inline_query(Var.BOT_USERNAME, f"msg {put}")
        except rep:
            return await eor(e, f"Bot tidak menanggapi inline kueri\nCoba lakukan `{HNDLR}restart`")
        except dis:
            return await eor(e, "Tolong aktifkan inline mode pada bot di @BotFather")
        await results[0].click(e.chat_id, reply_to=e.reply_to_msg_id, hide_via=True)
        await e.delete()
    else:
        await eor(e, "Berikan id atau username, atau bisa juga balas ke sebuah pesan")

@in_pattern("msg")
async def _(e):
    text = e.text
    okie = text.split(" ", maxsplit=1)
    mess = okie[1]
    try:
        sed = mess.split(" wspr ", maxsplit=1)
        query = sed[0]
    except IndexError:
        return
    quid = e.query.user_id
    try:
        desc = sed[1]
    except IndexError:
        desc = "Sentuh saya"
    if "wspr" not in text:
        try:
            logi = await king_bot(gu(id=query))
            name = logi.user.first_name
            ids = logi.user.id
            username = logi.user.username
            x = logi.user.status
            bio = logi.about
            if isinstance(x, on):
                status = "Online"
            if isinstance(x, off):
                status = "Offline"
            if isinstance(x, rec):
                status = "Terlihat baru-baru ini"
            if isinstance(x, lm):
                status = "Terakhir dilihat beberapa bulan yang lalu"
            if isinstance(x, lw):
                status = "Terakhir dilihat beberapa minggu yang lalu"
            if isinstance(x, mt):
                status = "Tidak bisa Berbicara"
            text =( f"**Name:** `{name}`\n"
                    f"**Id:** `{ids}`\n"
                    f"**Username:** `{username}`\n"
                    f"**Status:** `{status}`\n"
                    f"**About:** `{bio}`"
                    )
            button = [
                Button.url("Pc Dia", url=f"t.me/{username}"),
                Button.switch_inline(
                    "Pesan Rahasia",
                    query=f"msg {query} wspr ",
                    same_peer=True
                )
            ]
            builder = e.builder.article(
                title=f"{name}",
                description=desc,
                text=text,
                buttons=button
            )
        except BaseException:
            name = f"User {query} tidak ditemukan\nCari Lagi"
            builder = e.builder.article(
                title=name,
                text=name
            )
    else:
        try:
            logi = await king_bot.get_entity(query)
            button = [
                Button.inline("Pesan Rahasia", data=f"dd_{logi.id}"),
                Button.inline("Hapus Pesan", data=f"del")
            ]
            us = logi.username
            builder = e.builder.article(
                title=f"{logi.first_name}",
                description=desc,
                text=f"@{us} ini pesan rahasia untuk mu.\nHapus pesan setelah membacanya.\nAtau pesan selanjutnya tidak bisa diterima",
                buttons=button
            )
            userss.append(quid)
            userss.append(logi.id)
            reasons.update({logi.id: desc})
        except ValueError:
            builder = e.builder.article(
                title="Ketikkan pesan mu",
                text=f"Kamu belum mengetik pesan"
            )
    await e.builder([builder])


@callback(
    re.compile("dd_(.*)")
)
async def _(e):
    ids = int(e.pattern_match.group(1).decode("UTF-8"))
    if e.sender_id in userss:
        await e.answer(reasons[ids], allert=True)
    else:
        await e.answer("Gausa kepo, ini bukan buat kamu", alert=True)
        

@callback("del")
async def _(e):
    if e.sender_id in userss:
        for k in userss:
            try:
                del reasons[k]
                userss.clear()
            except KeyError:
                pass
            try:
                await e.edit("Pesan Dihapus!")
            except np:
                pass
    else:
        await e.answer("Kamu Tidak diizinkan untuk melakukan ini", alert=True)
