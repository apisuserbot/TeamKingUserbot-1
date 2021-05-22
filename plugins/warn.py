# King - UserBot
# Copyright (C) 2020 TeamKing
#
# This file is a part of < https://github.com/TeamKing/King/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamKing/King/blob/main/LICENSE/>.

"""
✘ Commands Available

•`{i}peringatan <balas ke pengguna> <alasan>`
    Memberi Peringatan.

•`{i}reset peringatan <balas ke pengguna>`
    Atau mereset semua peringatan.

•`{i}memperingatkan <balas ke pengguna>`
   Untuk Mendapatkan Daftar Peringatan dari pengguna.

•`{i}set peringatan dengan .warn <memperingatkan hitungan> | <ban/mute/kick>`
   Atur Nomor dalam hitungan peringatan untuk peringatan
   Setelah meletakkan " | " tandai menempatkan tindakan seperti ban/mute/kick
   Default-nya 3 kick
   Contoh : `set 5 peringatan | mute`

"""

from pyking.functions.warn_db import *
from telethon.utils import get_display_name

from . import *


@king_cmd(pattern="warn ?(.*)", groups_only=True, admins_only=True)
async def warn(e):
    reply = await e.get_reply_message()
    if len(e.text) > 5:
        if " " not in e.text[5]:
            return
    if reply:
        user = reply.from_id.user_id
        reason = "tidak dikenal"
        if e.pattern_match.group(1):
            reason = e.text[5:]
    else:
        try:
            user = e.text.split()[1]
            if user.startswith("@"):
                ok = await king_bot.get_entity(user)
                user = ok.id
            else:
                user = int(user)
        except BaseException:
            return await eod(e, "Reply To A User")
        try:
            reason = e.text.split(maxsplit=2)[-1]
        except BaseException:
            reason = "tidak dikenal"
    count, r = warns(e.chat_id, user)
    if not r:
        r = reason
    else:
        r = r + "|$|" + reason
    try:
        x = udB.get("SETWARN")
        number, action = int(x.split()[0]), x.split()[1]
    except BaseException:
        number, action = 3, "kick"
    if ("ban" or "kick" or "mute") not in action:
        action = "kick"
    if count + 1 >= number:
        if "ban" in action:
            try:
                await ultroid_bot.edit_permissions(e.chat_id, user, view_messages=False)
            except BaseException:
                return await eod(e, "`Ada yang salah.`")
        elif "kick" in action:
            try:
                await ultroid_bot.kick_participant(e.chat_id, user)
            except BaseException:
                return await eod(e, "`Ada yang salah.`")
        elif "mute" in action:
            try:
                await ultroid_bot.edit_permissions(
                    e.chat_id, user, until_date=None, send_messages=False
                )
            except BaseException:
                return await eod(e, "`Ada yang salah.`")
        add_warn(e.chat_id, user, count + 1, r)
        c, r = warns(e.chat_id, user)
        ok = await king_bot.get_entity(user)
        user = f"[{get_display_name(ok)}](tg://user?id={ok.id})"
        r = r.split("|$|")
        text = f"Pengguna {user} Punya {action} Disebabkan oleh {count+1} memperingatkan.\n\n"
        for x in range(c):
            text += f"•**{x+1}.** {r[x]}\n"
        await eor(e, text)
        return reset_warn(e.chat_id, ok.id)
    add_warn(e.chat_id, user, count + 1, r)
    ok = await king_bot.get_entity(user)
    user = f"[{get_display_name(ok)}](tg://user?id={ok.id})"
    await eor(
        e,
        f"**PERINGATAN :** {count+1}/{number}\n**Untuk :**{user}\n**Hati-hati !!!**\n\n**alasan** : {reason}",
    )


@king_cmd(pattern="resetwarn ?(.*)", groups_only=True, admins_only=True)
async def rwarn(e):
    reply = await e.get_reply_message()
    if reply:
        user = reply.from_id.user_id
    else:
        try:
            user = e.text.split()[1]
            if user.startswith("@"):
                ok = await king_bot.get_entity(user)
                user = ok.id
            else:
                user = int(user)
        except BaseException:
            return await eor(e, "Tolong Balas Ke Pengguna!")
    reset_warn(e.chat_id, user)
    ok = await king_bot.get_entity(user)
    user = f"[{get_display_name(ok)}](tg://user?id={ok.id})"
    await eor(e, f"Menghapus Semua Peringatan dari {user}.")


@king_cmd(pattern="warns ?(.*)", groups_only=True, admins_only=True)
async def twarns(e):
    reply = await e.get_reply_message()
    if reply:
        user = reply.from_id.user_id
    else:
        try:
            user = e.text.split()[1]
            if user.startswith("@"):
                ok = await king_bot.get_entity(user)
                user = ok.id
            else:
                user = int(user)
        except BaseException:
            return await eod(e, "Tolong Balas Ke Pengguna!")
    c, r = warns(e.chat_id, user)
    if c and r:
        ok = await king_bot.get_entity(user)
        user = f"[{get_display_name(ok)}](tg://user?id={ok.id})"
        r = r.split("|$|")
        text = f"Pengguna {user} Punya {c} memperingatkan.\n\n"
        for x in range(c):
            text += f"•**{x+1}.** {r[x]}\n"
        await eor(e, text)
    else:
        await eor(e, "`Tidak Memiliki Peringatan!`")


@king_cmd(pattern="setwarn ?(.*)")
async def warnset(e):
    ok = e.pattern_match.group(1)
    if not ok:
        return await eor(e, "stuff")
    if "|" in ok:
        try:
            number, action = int(ok.split()[0]), ok.split()[1]
        except BaseException:
            return await eod(e, "`Format Salah`")
        if ("ban" or "kick" or "mute") not in action:
            return await eod(e, "`Hanya mute / ban / kick opsi yang didukung`")
        udB.set("SETWARN", f"{number} {action}")
        return await eor(
            e, f"Selesai Hitungan Peringatan Anda sekarang {number} dan Aksi adalah {action}"
        )
    else:
        await eod(e, "`Format Salah`")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
