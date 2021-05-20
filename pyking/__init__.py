# KingUserbot
# Copyright (C) 2021 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.

import os
from redis import ConnectionError, ResponseError, StrictRedis
from telethon.errors import AuthKeyDuplicatedError
from telethon.sessions import StringSession
from telethon import TelegramClient
from logging import basicConfig, getLogger, INFO, DEBUG, warning as wr
from distutils.util import strtobool as sb
from decouple import config
from datetime import datetime

from .dB.database import Var
from .dB.core import *

from .functions import *
from .misc import *

LOGS = getLogger(__name__)

__version__ = "2021.04.14"

try:
    redis_info = Var.REDIS_URI.split(":")
    udB = StrictRedis(
        host=redis_info[0],
        port=redis_info[1],
        password=Var.REDIS_PASSWORD,
        charset="utf-8",
        decode_responses=True,
    )
except ConnectionError as ce:
    wr(f"ERROR - {ce}")
    exit(1)
except ResponseError as resps:
    wr(f"ERROR - {resps}")
    exit(1)


if not Var.API_ID or not Var.API_HASH:
    wr("Tidak Ada API_ID atau API_HASH. Sistem Dimatikan...")
    exit(1)

BOT_MODE = Var.BOT_MODE or udB.get("BOT_MODE")

if Var.SESSION:
    try:
        king_bot = TelegramClient(
            StringSession(Var.SESSION), Var.API_ID, Var.API_HASH
        )
    except Exception as excp:
        wr(f"ERROR - {excp}")
        exit(1)
elif str(BOT_MODE) == "True":
    try:
        king_bot = TelegramClient(None, api_id=Var.API_ID, api_hash=Var.API_HASH).start(bot_token=Var.BOT_TOKEN)
    except Exception as ap:
        wr(f"ERROR - {ap}")
        exit(1)
else:
    wr("Tidak Ada String Session, Sistem Dimatikan...")
    exit(1)

START_TIME = datetime.now()

if str(BOT_MODE) == "True" and not udB.get("OWNER_ID"):
    wr("ERROR - OWNER_ID Tidak Ditemukan ! Tolong tambahkan itu!")
    exit(1)

try:
    if udB.get("HNDLR"):
        HNDLR = udB.get("HNDLR")
    else:
        udB.set("HNDLR", ".")
        HNDLR = udB.get("HNDLR")
except BaseException as be:
    pass

if udB.get("SUDOS") is None:
    udB.set("SUDOS", "1")

if udB.get("VC_SESSION"):
    try:
        vcbot = TelegramClient(
            StringSession(udB.get("VC_SESSION")),
            api_id=Var.API_ID,
            api_hash=Var.API_HASH,
        )
    except AuthKeyDuplicatedError:
        wr("ERROR - Tolong buat session baru untuk bot vcg !")
        vcbot = None
    except Exception:
        vcbot = None
else:
    vcbot = None
