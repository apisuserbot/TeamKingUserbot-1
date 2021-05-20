#!/bin/bash
# King-Userbot - UserBot
# Copyright (C) 2020 TeamKing-Userbot
#
# This file is a part of < https://github.com/TeamKing-Userbot/King-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamKing-Userbot/King-Userbot/blob/main/LICENSE/>.


from telethon.sync import TelegramClient
from telethon.sessions import StringSession

from telethon.errors.rpcerrorlist import ApiIdInvalidError, PhoneNumberInvalidError

print("""Tolong pergi ke my.telegram.org
Login menggunakan akun telegram kamu
Klik pada API Development Tools
Buat aplikasi baru dan isi kolom nya
Cek Pesan Tersimpan Telegram kamu untuk copy STRING_SESSION""")
API_ID = int(input("Masukkan API_ID: "))
API_HASH = input("Masukkan API_HASH: ")

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("Cek Pesan Tersimpan Telegram kamu untuk copy STRING_SESSION ")
    session_string = client.session.save()
    saved_messages_template = """Grup Support @TeamKingUserbot

<code>STRING_SESSION</code>: <code>{}</code>

⚠️ <i>Please be careful before passing this value to third parties</i>""".format(session_string)
    client.send_message("me", saved_messages_template, parse_mode="html")
