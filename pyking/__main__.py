# KingUserbot
# Copyright (C) 2021 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.

import asyncio
import glob
import logging
from pathlib import Path

import telethon.utils
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.version import __version__ as vers
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError, PeerIdInvalidError
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.types import InputMessagesFilterDocument

from .utils import *
from . import *
from . import __version__ as ver
from .functions.all import AreUpdatesAvailable

# remove the old logs file.
if os.path.exists("ultroid.log"):
    os.remove("ultroid.log")

# start logging into a new file.
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("kingbot.log"), logging.StreamHandler()],
)

if not os.path.isdir("resources/auths"):
    os.mkdir("resources/auths")

if not os.path.isdir("resources/downloads"):
    os.mkdir("resources/downloads")

if not os.path.isdir("addons"):
    os.mkdir("addons")

token = udB.get("GDRIVE_TOKEN")
if token:
    with open("resources/auths/auth_token.txt", "w") as t_file:
        t_file.write(token)

websocket = udB.get("WEBSOCKET_URL")
if websocket:
    ulr = f"WEBSOCKET_URL={websocket}"
    with open(".env", "w") as t:
        t.write(ulr)


async def istart(king):
    await king_bot.start(king)
    king_bot.me = await king_bot.get_me()
    king_bot.uid = telethon.utils.get_peer_id(king_bot.me)
    king_bot.first_name = king_bot.me.first_name
    if not king_bot.me.bot:
        udB.set("OWNER_ID", king_bot.uid)
    if str(BOT_MODE) == "True":
        OWNER = await king_bot.get_entity(int(udB.get("OWNER_ID")))
        king_bot.me = OWNER
        asst.me = OWNER
        king_bot.uid = OWNER.id
        king_bot.first_name = OWNER.first_name

king_bot.asst = None


async def bot_info(botasst):
    await botasst.start()
    botasst.me = await botasst.get_me()
    return botasst.me


LOGS.info(
    """
                -------------------------------------
                            Memulai Deploy
                -------------------------------------
"""
)

LOGS.info("Meng-Inisialisasi")
LOGS.info(f"pyking Versi - {ver}")
LOGS.info(f"Telethon Versi - {vers}")
LOGS.info("King-Userbot Versi - 1.0.0")

if str(BOT_MODE) == "True":
    mode = "Bot Mode Dimulai"
else:
    mode = "User Mode Dimulai"

if Var.BOT_TOKEN is not None:
    LOGS.info("Memulai King-Userbot")
    try:
        king_bot.asst = TelegramClient(
            None, api_id=Var.API_ID, api_hash=Var.API_HASH
        ).start(bot_token=Var.BOT_TOKEN)
        asst = king_bot.asst
        king_bot.loop.run_until_complete(istart(asst))
        king_bot.loop.run_until_complete(bot_info(asst))
        LOGS.info("Selesai, startup telah beres")
    except AuthKeyDuplicatedError:
        LOGS.info(
            "Ganti Session String anda"
        )
        exit(1)
    except BaseException as e:
        LOGS.info("Error: " + str(e))
        exit(1)
else:
    LOGS.info(mode)
    king_bot.start()

udB.set("OWNER_ID", king_bot.uid)

BOTINVALID_PLUGINS = [
    "globaltools",
    "autopic",
    "pmpermit",
    "fedutils",
    "_tagnotifs",
    "webupload",
    "clone",
    "inlinefun",
    "tscan",
    "animedb",
    "limited",
    "quotly",
    "findsong",
    "sticklet",
]


# For userbot
path = "plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        try:
            if str(BOT_MODE) == "True" and plugin_name in BOTINVALID_PLUGINS:
                LOGS.info(
                    f"King-Userbot - Official - BOT_MODE_INVALID_PLUGIN - {plugin_name}"
                )
            else:
                load_plugins(plugin_name.replace(".py", ""))
                if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                    LOGS.info(f"King-Userbot  -  Official  -  Terinstall  -  {plugin_name}")
        except Exception as e:
            LOGS.info(f"King-Userbot  -  Official  -  ERROR  -  {plugin_name}")
            LOGS.info(str(e))


# For Addons
addons = udB.get("ADDONS")
if addons == "True" or addons is None:
    os.system("git clone https://github.com/DoellBarr/King-UserbotAddons.git addons/")
    LOGS.info("Meng-Install package untuk addons")
    os.system("pip install -r ./addons/addons.txt")
    path = "addons/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            try:
                if str(BOT_MODE) == "True" and plugin_name in BOTINVALID_PLUGINS:
                    LOGS.info(
                        f"King-Userbot - Official - BOT_MODE_INVALID_PLUGIN - {plugin_name}"
                    )
                else:
                    load_plugins(plugin_name.replace(".py", ""))
                    if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                        LOGS.info(f"King-Userbot  -  Official  -  Terinstall  -  {plugin_name}")
                    LOGS.info(f"King-Userbot  -  Addons  -  Terinstall  -  {plugin_name}")
            except Exception as e:
                LOGS.warning(f"King-Userbot  -  Addons  -  ERROR  -  {plugin_name}")
else:
    os.system("cp plugins/__init__.py addons/")
    
    
# For assistant
path = "assistant/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        try:
            load_addons(plugin_name.replace(".py", ""))
            if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                LOGS.info(f"King-Userbot  -  Assistant  -  Terinstall  -  {plugin_name}")
        except Exception as e:
            LOGS.warning(f"King-Userbot  -  Assistant  -  ERROR  -  {plugin_name}")


# For channel plugin
Plug_channel = udB.get("PLUGIN_CHANNEL")
if Plug_channel:
    
    async def plug():
        try:
            try:
                if not Plug_channel.startswith("/"):
                    chat = int(Plug_channel)
                else:
                    return
            except BaseException:
                if Plug_channel.startswith("@"):
                    chat = Plug_channel
                else:
                    return
            plugins = await king_bot.get_messages(
                chat,
                None,
                search=".py",
                filter=InputMessagesFilterDocument,
            )
            total = int(plugins.total)
            totals = range(0, total)
            for ult in totals:
                uid = plugins[ult].id
                file = await king_bot.download_media(
                    await king_bot.get_messages(chat, ids=uid), "./addons/"
                )
                if "(" not in file:
                    upath = Path(file)
                    name = upath.stem
                    try:
                        load_addons(name.replace(".py", ""))
                        LOGS.info(
                            f"King-Userbot - PLUGIN_CHANNEL - Terinstall - {(os.path.basename(file))}"
                        )
                    except Exception as e:
                        LOGS.warning(
                            f"King-Userbot - PLUGIN_CHANNEL - ERROR - {(os.path.basename(file))}"
                        )
                        LOGS.warning(str(e))
                else:
                    LOGS.info(f"Plugin {(os.path.basename(file))} sudah pernah terinstall")
                    os.remove(file)
        except Exception as e:
            LOGS.warning(str(e))
            
    async def modif_bot():
        try:
            entit = await king_bot.get_entity(Var.BOT_USERNAME)
            if entit.photo == None:
                LOGS.info("Meng-Kustomisasi Bot Assistant anda di @BotFather")
                uname = Var.BOT_USERNAME
                if uname.startswith("@"):
                    UL = uname
                else:
                    UL = f"@{uname}"
                if king_bot.me.username == None:
                    first_name = king_bot.me.first_name
                else:
                    first_name = f"@{king_bot.me.username}"
                await king_bot.send_message(
                    Var.LOG_CHANNEL, "Kustomisasi Otomatis Berjalan di @BotFather"
                )
                await asyncio.sleep(1)
                await king_bot.send_message("botfather", "/cancel")
                await asyncio.sleep(1)
                await king_bot.send_message("botfather", "/start")
                await asyncio.sleep(1)
                await king_bot.send_message("botfather", "/setuserpic")
                await asyncio.sleep(1)
                await king_bot.send_message("botfather", UL)
                await asyncio.sleep(1)
                await king_bot.send_file("botfather", "resources/extras/kingbot_assistant.jpg")
                await asyncio.sleep(2)
                await king_bot.send_message("botfather", "/setabouttext")
                await asyncio.sleep(1)
                await king_bot.send_message("botfather", UL)
                await asyncio.sleep(1)
                await king_bot.send_message(
                    "botfather", f"✨Haii✨!! Saya Asisten bot dari {first_name}"
                )
                await asyncio.sleep(2)
                await king_bot.send_message("botfather", "/setdescription")
                await asyncio.sleep(1)
                await king_bot.send_message("botfather", UL)
                await asyncio.sleep(1)
                await king_bot.send_message(
                    "botfather",
                    f"✨King-Userbot Assistant Bot✨\n✨Mastah ~ {first_name} ✨\n\n✨Powered By ~ @TeamKingUserbot✨",
                )
                await asyncio.sleep(2)
                await king_bot.send_message("botfather", "/start")
                await asyncio.sleep(1)
                await king_bot.send_message(
                    Var.LOG_CHANNEL, "**Kustomisasi otomatis** Selesai dilakukan di @BotFather"
                )
                LOGS.info("Kustomisasi Selesai")
        except Exception as e:
            LOGS.warning(str(e))


async def has_deploy():
    if Var.LOG_CHANNEL:
        try:
            try:
                await king_bot(AddChatUserRequest(chat_id=Var.LOG_CHANNEL, user_id=asst.me.username, fwd_limit=10))
            except BaseException:
                try:
                    await king_bot(InviteToChannelRequest(channel=Var.LOG_CHANNEL, users=[asst.me.username]))
                except PeerIdInvalidError:
                    LOGS.warning("ID Channel/Group didalam vars LOG_CHANNEl SALAH")
                except BaseException as ep:
                    LOGS.info(ep)

            BTTS = None
            updava = await AreUpdatesAvailable()
            if updava:
                BTTS = [[Button.inline(text="Update Tersedia", data="updtava")]]
            await king_bot.asst.send_message(
                Var.LOG_CHANNEL,
                f"**King-Userbot sudah di deploy!**\n"
                f"➖➖➖➖➖➖➖➖➖\n"
                f"**Userbot:** [{king_bot.me.first_name}](tg://user?id={king_bot.me.id})\n"
                f"**Assisten:** @{asst.me.username}\n"
                f"➖➖➖➖➖➖➖➖➖\n"
                f"**Support:**@TeamKingUserbot\n"
                f"➖➖➖➖➖➖➖➖➖",
                buttons=BTTS
            )
        except BaseException:
            try:
                await king_bot.send_message(
                    Var.LOG_CHANNEL,
                    f"**King-Userbot sudah di deploy!**\n➖➖➖➖➖➖➖➖➖\n**Userbot:** [{king_bot.me.first_name}](tg://user?id={king_bot.me.id})\n**Assisten:** {UL}\n➖➖➖➖➖➖➖➖➖\n**Support:**@TeamKingUserbot\n➖➖➖➖➖➖➖➖➖",
                )
            except BaseException:
                pass
    try:
        await king_bot(JoinChannelRequest("@TeamKingUserbot"))
    except BaseException:
        pass

if str(BOT_MODE) != "True":
    king_bot.loop.run_until_complete(modif_bot())
    if Plug_channel:
        king_bot.loop.run_until_complete(plug())
king_bot.loop.run_until_complete(has_deploy())

LOGS.info(
    """
    ---------------------------------------------------------------------------------------
        King-Userbot telah di deploy! Kunjungin @TeamKingUserbot untuk update terbaru
    ---------------------------------------------------------------------------------------
    """
)

if __name__ == "__main__":
    king_bot.run_until_disconnected()
