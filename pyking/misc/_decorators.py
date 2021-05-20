# KingUserbot
# Copyright (C) 2021 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.

import re
import inspect
import sys
import asyncio
import requests

from sys import *
from os import remove
from pathlib import Path
from traceback import format_exc
from time import gmtime, strftime, sleep
from asyncio import create_subprocess_shell as asyncsubshell, subprocess as asyncsub

from .. import *
from ..dB.core import *
from ..dB.database import Var
from ..functions.all import time_formatter as tf
from ..utils import *
from telethon import *
from telethon.errors.rpcerrorlist import (
    FloodWaitError,
    MessageIdInvalidError,
    MessageNotModifiedError,
)
from ._wrappers import *

# Sudo
ok = udB["SUDOS"]
if ok:
    SUDO_USERS = set(int(x) for x in ok.split())
else:
    SUDO_USERS = ""

if SUDO_USERS:
    sudos = list(SUDO_USERS)
else:
    sudos = ""

on = udB["SUDO"] if udB["SUDO"] is not None else "False"

if on == "True":
    sed = [king_bot.uid, *sudos]
else:
    sed  = [king_bot.uid]

hndlr = "\\" + HNDLR

kek = udB.get("SUDO_PLUGINS")

if kek:
    SUDO_ALLOWED_PLUGINS = set(str(x) for x in kek.split(" "))
else:
    SUDO_ALLOWED_PLUGINS = ""

if SUDO_ALLOWED_PLUGINS:
    sudoplugs = list(SUDO_ALLOWED_PLUGINS)
else:
    sudoplugs = ""

# Decorator


def king_cmd(allow_sudo=on, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args.get("pattern", None)
    groups_only = args.get("groups_only", False)
    admins_only = args.get("admins_only", False)
    disable_errors = args.get("disable_errors", False)
    # args["outgoing"] = True
    #
    # if allow_sudo == "True":
    #     args["from_users"] = sed
    #     args["incoming"] = True
    #
    # else:
    #     args["outgoing"] = True

    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = re.compile(pattern)
        else:
            args["pattern"] = re.compile(hndlr + pattern)
        reg = re.compile("(.*)")
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = (
                    cmd.group(1)
                    .replace("$", "")
                    .replace("?(.*)", "")
                    .replace("(.*)", "")
                    .replace("(?: |)", "")
                    .replace("| ", "")
                    .replace("( |)", "")
                    .replace("?((.|//)*)", "")
                    .replace("?P<shortname>\\w+", "")
                )
            except:
                pass
            try:
                LIST[file_test].append(cmd)
            except:
                LIST.update({file_test: [cmd]})
        except:
            pass
    args["blacklist_chats"] = True
    black_list_chats = list(Var.BLACKLIST_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats

    # Cek jika plugin harus menyetujui edited update
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        args["allow_edited_updates"]
        del args["allow_edited_updates"]
    if "admins_only" in args:
        del args["admins_only"]
    if "groups_only" in args:
        del args["groups_only"]

    # Cek jika plugin harus menunggu untuk pesan terkirim

    def decorator(func):
        async def wrapper(king):
            if allow_sudo == "False":
                if not king.out:
                    return
            if not king.out and (king.sender_id not in sudos):
                return
            chat = await king.get_chat()
            if king.fwd_from:
                return
            if groups_only and king.is_private:
                return await eod(king, "`Gunakan ini di channel/grup.`", time=3)
            if admins_only and not chat.admin_rights:
                return await eod(king, "`Saya bukan admin.`", time=3)
            try:
                await func(king)
            except MessageIdInvalidError:
                pass
            except MessageNotModifiedError:
                pass
            except FloodWaitError as fwerr:
                await king_bot.asst.send_message(
                    Var.LOG_CHANNEL,
                    f"`FloodWaitError:\n{str(fwerr)}\n\nBot tidur sementara selama {tf((fwerr.seconds + 10)*1000)}`",
                )
                sleep(fwerr.seconds + 10)
                await king_bot.asst.send_message(
                    Var.LOG_CHANNEL,
                    "`Bot sudah bisa digunakan lagi`",
                )
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException as bexc:
                LOGS.exception(bexc)
                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = f"""
        **KingBot - Laporan Error!!!**
        Abaikan ini atau laporkan ke @KingUserbotSupport.
        """
                    ftext = f"""
                    \nDisclaimer:\nFile ini HANYA di upload disini saja,
                    kami hanya menerima sinyal error dan tanggal, kami menghargai privasi anda,
                    anda tidak perlu melaporkan error ini jika anda mau
                    --------START KING BOT CRASH LOG--------
                    \nTanggal: {date}
                    \nId Grup: {str(king.chat_id)}
                    \nId Pengirim: {str(king.sender_id)}
                    \n\nEvent Trigger:
                    \n{str(king.text)}
                    \n\nInfo Traceback:
                    \n{str(format_exc())}
                    \n\nText Error:
                    \n{str(sys.exc_info()[1])}
                    \n\n--------END KING BOT CRASH LOG--------"""

                    command = 'git log --pretty=format:"%an: %s" -5'

                    text += "\n\n\n5 Commit terakhir:\n"

                    process = await asyncsubshell(
                        command, stdout=asyncsub.PIPE, stderr=asyncsub.PIPE
                    )
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) + str(stderr.decode().strip())

                    ftext += result

                    file = open("kingbot-log.txt", "w+")
                    file.write(ftext)
                    file.close()
                    key = (
                        requests.post(
                            "https://nekobin.com/api/documents", json={"content": ftext}
                        )
                        .json()
                        .get("result")
                        .get("key")
                    )
                    url = f"https://nekobin.com/{key}"
                    text += f"\nDi Paste [disini]({url}) juga."
                    if Var.LOG_CHANNEL:
                        Placetosend = Var.LOG_CHANNEL
                    else:
                        Placetosend = king_bot.uid
                    await king_bot.asst.send_file(
                        Placetosend,
                        "ultroid-log.txt",
                        caption=text,
                    )
                    remove("ultroid-log.txt")
        king_bot.add_event_handler(wrapper, events.NewMessage(**args))
        try:
            LOADED[file_test].append(wrapper)
        except Exception:
            LOADED.update({file_test: [wrapper]})
        return wrapper

    return decorator
