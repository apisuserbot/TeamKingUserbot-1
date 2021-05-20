# King-Userbot
# Copyright (C) 2021 TeamKingUserbot
#
# This file is a part of < https://github.com/DoellBarr/TeamKing-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/DoellBarr/TeamKing-Userbot/blob/main/LICENSE/>.

"""
✘ Commands Available -

• `{i}afk <alasan opsional>`
    AFK berarti Away From Keyboard,
    Setelah anda mengaktifkan ini, jika ada seseorang men=tag atau chat anda, lalu secara otomatis, bot akan membalasnya,
    (Catatan : Dengan membalas ke media apapun, anda bisa menyetel media afk juga).

"""

# • `{i}afk <alasan opsional> | <nama belakang>`
#     Sama seperti {i}afk, tetapi ini akan merubah nama belakang anda sesuai apa yang diinginkan,
#     (Contoh : {i}afk tarawih | OFF)

# TODO Menambahkan Custom Offline text di Nama Belakang

import asyncio

from telethon import events
from telethon.tl import functions, types
from telethon.tl.functions.account import UpdateProfileRequest

from pyking.misc._decorators import king_cmd
from ..pyking import *
from ..pyking.functions.pmpermit_db import is_approved

global USER_AFK
global afk_time
global last_afk_message
global last_afk_msg
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
last_afk_message = {}
last_afk_msg = {}
afk_start = {}

LOG = Var.LOG_CHANNEL


@king_bot.on(events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
async def on_afk(event):
    if event.fwd_from:
        return
    if event.is_private:
        if not is_approved(event.chat_id):
            return
    global USER_AFK
    global total_afk_time
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str(afk_end - afk_start)
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        return False
    sender = await event.get_sender()
    if USER_AFK and not (sender.bot or sender.verified):
        msg = None
        if reason:
            message_to_reply = f"Sedang Offline\nTerakhir dilihat {total_afk_time}\n**Karena:** {reason}"
        else:
            message_to_reply = f"Lagi Off Dulu, Terakhir dilihat {total_afk_time}"
        try:
            if pic.endswith((".tgs", ".webp")):
                msg = await event.reply(file=pic)
                msgs = await event.reply(message_to_reply)
            else:
                msg = await event.reply(message_to_reply, file=pic)
        except BaseException:
            msg = await event.reply(message_to_reply)
        await asyncio.sleep(2.5)
        if event.chat_id in last_afk_message:
            await last_afk_message[event.chat_id].delete()
        try:
            if event.chat_id in last_afk_msg:
                await last_afk_msg[event.chat_id].delete()
        except BaseException:
            pass
        last_afk_message[event.chat_id] = msg
        try:
            if msgs:
                last_afk_msg[event.chat_id] = msgs
        except BaseException:
            pass


@king_bot.on(events.NewMessage(outgoing=True))
@king_bot.on(events.MessageEdited(outgoing=True))
async def set_not_afk(event):
    global USER_AFK, total_afk_time
    global afk_time
    global last_afk_message
    global last_afk_msg
    global afk_start
    global afk_end
    global shites
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str(afk_end - afk_start)
    current_message = event.message.message
    if "afk" not in current_message and "yes" in USER_AFK:
        try:
            if pic.endswith((".tgs", ".webp")):
                shite = await king_bot.send_message(event.chat_id, file=pic)
                shites = await king_bot.send_message(event.chat_id, f"Tidak lagi afk setelah {total_afk_time}")
            else:
                shite = await king_bot.send_message(event.chat_id, f"Tidak lagi afk setelah {total_afk_time}", file=pic)
        except BaseException:
            shite = await king_bot.send_message(event.chat_id, f"Tidak lagi afk setelah {total_afk_time}")
        try:
            try:
                if pic.endswith((".tgs", ".webp")):
                    await king_bot.send_message(LOG, file=pic)
                    await king_bot.send_message(LOG, f"#AFK\nMenyetel AFK mode ke False.\nAFK untuk {total_afk_time}`")
                else:
                    await king_bot.send_message(LOG, f"#AFK\nMenyetel AFK mode ke False.\nAFK untuk {total_afk_time}`",
                                                file=pic)
            except BaseException:
                await king_bot.send_message(LOG, f"#AFK\nMenyetel AFK mode ke False.\nAFK untuk {total_afk_time}`")
        except BaseException:
            pass
        await asyncio.sleep(3)
        await shite.delete()
        try:
            await shites.delete()
        except BaseException:
            pass
        USER_AFK = {}
        afk_time = None


@king_cmd(pattern=r"afk ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    global USER_AFK
    global afk_time
    global last_afk_message
    global last_afk_msg
    global afk_start
    global afk_end
    global reason
    global pic
    user = await king_bot.get_me()
    USER_AFK = {}
    afk_time = None
    last_afk_message = {}
    last_afk_msg = {}
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    reason = event.pattern_match.group(1)
    if reply:
        pic = await event.client.download_media(reply)
    else:
        pic = None
    if not USER_AFK:
        last_seen_status = await king_bot(functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp()))
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.now()
        USER_AFK = f"yes: {reason} {pic}"
        if reason:
            try:
                if pic.endswith((".tgs", ".webp")) and user.last_name:
                    await king_bot.send_message(event.chat_id, file=pic)
                    await king_bot.send_message(event.chat_id, f"`Sedang AFK`\n\n**Karena:** {reason}")
                    if user.last_name:
                        await event.client(
                            UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                    else:
                        await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
                else:
                    await king_bot.send_message(event.chat_id, f"`Sedang AFK`\n\n**Karena:** {reason}", file=pic)
                    await event.client(
                        UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                    if user.last_name:
                        await event.client(
                            UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                    else:
                        await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
            except BaseException:
                await king_bot.send_message(event.chat_id, f"`Sedang AFK`\n\n**Karena:** {reason}")
                if user.last_name:
                    await event.client(
                        UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                else:
                    await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
        else:
            try:
                if pic.endswith((".tgs", ".webp")):
                    await king_bot.send_message(event.chat_id, file=pic)
                    await king_bot.send_message(event.chat_id, f"Sedang **OFFLINE**")
                    if user.last_name:
                        await event.client(
                            UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                    else:
                        await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
                else:
                    await king_bot.send_message(event.chat_id, f"Sedang **OFFLINE**")
                    if user.last_name:
                        await event.client(
                            UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                    else:
                        await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
            except BaseException:
                await king_bot.send_message(event.chat_id, f"Sedang **OFFLINE**")
                if user.last_name:
                    await event.client(
                        UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                else:
                    await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
        await event.delete()
        try:
            if reason and pic:
                if pic.endswith((".tgs", ".webp")):
                    await king_bot.send_message(LOG, file=pic)
                    await king_bot.send_message(LOG, f"Sedang **OFFLINE**\nKarena: {reason}")
                    if user.last_name:
                        await event.client(
                            UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                    else:
                        await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
                else:
                    await king_bot.send_message(LOG, f"Sedang **OFLINE**\nKarena: {reason}", file=pic)
                    if user.last_name:
                        await event.client(
                            UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                    else:
                        await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
            elif reason:
                await king_bot.send_message(LOG, f"Sedang **OFFLINE**\nKarena: {reason}")
                if user.last_name:
                    await event.client(
                        UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                else:
                    await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
            elif pic:
                if pic.endswith((".tgs", ".webp")):
                    await king_bot.send_message(LOG, file=pic)
                    await king_bot.send_message(LOG, "`Lagi Offline`")
                    if user.last_name:
                        await event.client(
                            UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                    else:
                        await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
                else:
                    await king_bot.send_message(LOG, "`Lagi Offline`", file=pic)
                    if user.last_name:
                        await event.client(
                            UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                    else:
                        await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
            else:
                await king_bot.send_message(LOG, "`Lagi Offline, Jangan Spam`")
                if user.last_name:
                    await event.client(
                        UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + "[𝓐𝓕𝓚]"))
                else:
                    await event.client(UpdateProfileRequest(first_name=user.first_name, last_name="[𝓐𝓕𝓚]"))
        except BaseException:
            pass


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
