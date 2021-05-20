# KingUserbot
# Copyright (C) 2021 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.
import asyncio
import heroku3
import httplib2
import io
import math
import os
import random
import re
import requests
import sys
import time
import urllib

from math import sqrt
from mimetypes import guess_type
from pathlib import Path

from git import Repo, NoSuchPathError, GitCommandError, InvalidGitRepositoryError
from html_telegraph_poster import TelegraphPoster
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    DownloadError,
    ContentTooShortError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from PIL import Image
from bs4 import BeautifulSoup as bs
from emoji import emojize
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from telegraph import Telegraph

from telethon import events
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    MessageActionChannelMigrateFrom,
    MessageEntityMentionName,
)
from telethon.utils import get_input_location
from ._FastTelethon import download_file as downloadable, upload_file as uploadable

from ..misc import *
from ..misc._wrappers import *
from ..utils import *

OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.file"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
parent_id = udB.get("GDRIVE_FOLDER_ID")
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"

telegraph = Telegraph()
telegraph.create_account(short_name="Daftar Perintah King-Userbot")


capt_version = "1.0.0"

CMD_WEB = {
    "anonfiles": 'curl -F "file=@{}" https://api.anonfiles.com/upload',
    "transfer": 'curl --upload-file "{}" https://transfer.sh/',
    "bayfiles": 'curl -F "file=@{}" https://api.bayfiles.com/upload',
    "x0": 'curl -F "file=@{}" https://x0.at/',
    "file.io": 'curl -F "file=@{}" https://file.io',
    "siasky": 'curl -X POST "https://siasky.net/skynet/skyfile" -F "file=@{}"',
}

UPSTREAM_REPO_URL = "https://github.com/DoellBarr/CaptainUserbot"

requirements_path = "resources/extras/local-requirements.txt"


async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def gen_chlog(repo, diff):
    ac_br = repo.active_branch.name
    ch_log = tldr_log = ""
    ch = f"<b>Captain {capt_version} update untuk <a href={UPSTREAM_REPO_URL}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    ch_tl = f"Captain {capt_version} update untuk {ac_br}"
    d_form = "%d/$m/$y || $H:$M"
    for c in repo.iter_commits(diff):
        ch_log += f"\n\n💬 <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b><a href={UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
        tldr_log += f"\n\n💬 {c.count()} 🗓 [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] 👨‍💻 {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    else:
        return ch_log, tldr_log


async def AreUpdatesAvailable():
    off_repo = UPSTREAM_REPO_URL
    try:
        repo = Repo()
    except NoSuchPathError as error:
        await king_bot.asst.send_message(
            Var.LOG_CHANNEL, f"{txt}\n `folder {error} tidak ditemukan`"
        )
        repo.__del__()
        return
    except GitCommandError as error:
        await king_bot.asst.send_message(
            Var.LOG_CHANNEL, f"{txt}\n `Kegagalan di awal! {error}`"
        )
        repo.__del__()
        return
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("dev", origin.refs.dev)
        repo.heads.dev.set_tracking_branch(origin.refs.dev)
        repo.heads.dev.checkout(True)
    ac_br = repo.active_branch.name
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if changelog:
        Avali = True
    else:
        Avali = False
    return Avali


async def updater(txt):
    off_repo = UPSTREAM_REPO_URL
    try:
        repo = Repo()
    except NoSuchPathError as error:
        await king_bot.asst.send_message(
            Var.LOG_CHANNEL, f"{txt}\n`folder {error} tidak ditemukan`"
        )
        repo.__del__()
        return
    except GitCommandError as error:
        await king_bot.asst.send_message(
            Var.LOG_CHANNEL, f"{txt}\n`Kegagalan di awal! {error}`"
        )
        repo.__del__()
        return
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("dev", origin.refs.dev)
        repo.heads.dev.set_tracking_branch(origin.refs.dev)
        repo.heads.dev.checkout(True)
    ac_br = repo.active_branch.name
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if changelog:
        msg = await king_bot.asst.send_file(
            Var.LOG_CHANNEL,
            "resources/extras/logo_rdm.png",
            caption="**0.0.6 Update tersedia**",
            force_document=True,
            buttons=Button.inline("Changelogs", data="changes"),
        )
    else:
        msg = None
    return msg


async def downloader(filename, file, event, taime, msg):
    with open(filename, "wb") as fk:
        result = await downloadable(
            client=event.client,
            location=file,
            out=fk,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d,
                    t,
                    event,
                    taime,
                    msg,
                ),
            ),
        )
    return result


def make_html_telegraph(title, author, text):
    client = TelegraphPoster(use_api=True)
    client.create_api_token(title)
    page = client.post(
        title=title,
        author=author,
        author_url="https://t.me/lvufrvrbby",
        text=text
    )
    return page["url"]


async def get_user_id(ids):
    if str(ids).isdigit():
        userid = int(ids)
    else:
        userid = (await king_bot.get_entity(ids)).id
    return userid


async def dloader(e, host, file):
    selected = CMD_WEB[host].format(file)
    process = await asyncio.create_subprocess_shell(
        selected, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    os.remove(file)
    return await e.edit(f"`{stdout.decode()}`")


def unlucks(unluck):
    if unluck == "msgs":
        rights = types.ChatBannedRights(
            until_date=None,
            send_messages=False,
            invite_users=False,
            pin_messages=False,
            change_info=False,
        )
    if unluck == "media":
        rights = types.ChatBannedRights(
            until_date=None,
            send_media=False,
        )
    if unluck == "sticker":
        rights = types.ChatBannedRights(
            until_date=None,
            send_stickers=False,
        )
    if unluck == "gif":
        rights = types.ChatBannedRights(
            until_date=None,
            send_gifs=False,
        )
    if unluck == "games":
        rights = types.ChatBannedRights(
            until_date=None,
            send_games=False,
        )
    if unluck == "inlines":
        rights = types.ChatBannedRights(
            until_date=None,
            send_inline=False,
        )
    if unluck == "polls":
        rights = types.ChatBannedRights(
            until_date=None,
            send_polls=False,
        )
    if unluck == "invites":
        rights = types.ChatBannedRights(
            until_date=None,
            invite_users=False,
        )
    if unluck == "pin":
        rights = types.ChatBannedRights(
            until_date=None,
            pin_messages=False,
        )
    if unluck == "changeinfo":
        rights = types.ChatBannedRights(
            until_date=None,
            change_info=False,
        )
    return rights


def lucks(luck):
    if luck == "msgs":
        rights = types.ChatBannedRights(
            until_date=None,
            send_messages=True,
            invite_users=True,
            pin_messages=True,
            change_info=True,
        )
    if luck == "media":
        rights = types.ChatBannedRights(
            until_date=None,
            send_media=True,
        )
    if luck == "sticker":
        rights = types.ChatBannedRights(
            until_date=None,
            send_stickers=True,
        )
    if luck == "gif":
        rights = types.ChatBannedRights(
            until_date=None,
            send_gifs=True,
        )
    if luck == "games":
        rights = types.ChatBannedRights(
            until_date=None,
            send_games=True,
        )
    if luck == "inlines":
        rights = types.ChatBannedRights(
            until_date=None,
            send_inline=True,
        )
    if luck == "polls":
        rights = types.ChatBannedRights(
            until_date=None,
            send_polls=True,
        )
    if luck == "invites":
        rights = types.ChatBannedRights(
            until_date=None,
            invite_users=True,
        )
    if luck == "pin":
        rights = types.ChatBannedRights(
            until_date=None,
            pin_messages=True,
        )
    if luck == "changeinfo":
        rights = types.ChatBannedRights(
            until_date=None,
            change_info=True,
        )
    return rights


async def ban_time(event, time_str):
    global time_int
    if any(time_str.endswith(unit) for unit in ("m", "j", "h")):
        unit = time_str[-1]
        time_int = time_str[:-1]
        if not time_int.isdigit():
            return await event.edit("Waktu yang diberikan invalid.")
        if unit == "m":
            bantime = int(time.time() + int(time_int) * 60)
        elif unit == "j":
            bantime = int(time.time() + int(time_int) * 60 * 60)
        elif unit == "h":
            bantime = int(time.time() + int(time_int) * 24 * 60 * 60)
        else:
            return ""
        return bantime
    else:
        return await event.edit(f"Tipe waktu yang diberikan salah. Harusnya m, j, atau h, dapat: {time_int[-1]}")


# GDrive


def list_files(http):
    drive = build("drive", "v2", http=http, cache_discovery=False)
    x = drive.files().get(fileId="").execute()
    files = {}
    for m in x["items"]:
        try:
            files.update({f"{m['title']}": f"{m['webContentLink']}"})
        except KeyError:
            pass
    lists = f"**Total File yang Ditemukan di Gdrive:** `{len(files.keys())}`\n\n"
    for l in files:
        lists += f"• [{l}]({files[l]})\n"
    return lists


async def gsearch(http, query, filename):
    drive_service = build("drive", "v2", http=http)
    page_token = None
    msg = "**Pencarian GDrive:**\n`" + filename + "`\n\n**Hasil**\n"
    while True:
        response = (
            drive_service.files()
            .list(
                q=query,
                spaces="drive",
                fields="nextPageToken, items(id, title, mimeType)",
                pageToken=page_token,
            )
            .execute()
        )
        for file in response.get("items", []):
            if file.get("mimeType") == "application/vnd.google-apps.folder":
                msg += (
                    "[{}](https://drive.google.com/drive/folders/{}) (folder)".format(
                        file.get("title"), file.get("id")
                    )
                    + "\n"
                )
            else:
                msg += (
                    "[{}](https://drive.google.com/uc?id={}&export=download)".format(
                        file.get("title"), file.get("id")
                    )
                    + "\n"
                )
        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break
    return msg


async def create_directory(http, directory_name, parent_id):
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True,
    }
    file_metadata = {
        "title": directory_name,
        "mimeType": G_DRIVE_DIR_MIME_TYPE,
    }
    if parent_id is not None:
        file_metadata["parents"] = [{"id": parent_id}]
    file = drive_service.files().insert(body=file_metadata).execute()
    file_id = file.get("id")
    drive_service.permissions().insert(fileId=file_id, body=permissions).execute()
    return file_id


async def DoTeskWithDir(http, input_directory, event, parent_id):
    list_dirs = os.listdir(input_directory)
    if len(list_dirs) == 0:
        return parent_id
    r_p_id = None
    for a_c_f_name in list_dirs:
        current_file_name = os.path.join(input_directory, a_c_f_name)
        if os.path.isdir(current_file_name):
            current_dir_id = await create_directory(http, a_c_f_name, parent_id)
            r_p_id = await DoTeskWithDir(http, current_file_name, event, current_dir_id)
        else:
            file_name, mime_type = file_ops(current_file_name)
            g_drive_link = await upload_file(
                http, current_file_name, file_name, mime_type, event, parent_id
            )
            r_p_id = parent_id
    return r_p_id


def file_ops(file_path):
    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"
    file_name = file_path.split("/")[-1]
    return file_name, mime_type


async def create_token_file(token_file, event):
    flow = OAuth2WebServerFlow(
        udB.get("GDRIVE_CLIENT_ID"),
        udB.get("GDRIVE_CLIENT_SECRET"),
        OAUTH_SCOPE,
        redirect_uri=REDIRECT_URI,
    )
    authorize_url = flow.step1_get_authorize_url()
    async with king_bot.asst.conversation(king_bot.uid) as conv:
        await event.edit(
            f"Pergi ke link yang diberikan: [Authorization Link]({authorize_url}) dan balas dengan code yang diberikan",
            link_preview=False,
        )
        response = conv.wait_event(events.NewMessage(from_users=king_bot.uid))
        response = await response
        code = response.message.message.strip()
        credentials = flow.step2_exchange(code)
        storage = Storage(token_file)
        storage.put(credentials)
        return storage


def authorize(token_file, storage):
    if storage is None:
        storage = Storage(token_file)
    credentials = storage.get()
    http = httplib2.Http()
    credentials.refresh(http)
    http = credentials.authorize(http)
    return http


async def upload_file(http, file_path, file_name, mime_type, event, parent_id):
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    media_body = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    body = {
        "title": file_name,
        "description": "Di upload menggunakan King-Userbot",
        "mimeType": mime_type,
    }
    if parent_id is not None:
        body["parents"] = [{"id": parent_id}]
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True,
    }
    file_size = os.path.getsize(file_path)
    file = drive_service.files().insert(body=body, media_body=media_body)
    times = time.time()
    response = None
    display_message = ""
    while response is None:
        status, response = file.next_chunk(num_retries=5)
        if status:
            t_size = status.total_size
            diff = time.time() - times
            uploaded = status.resumable_progress
            percentage = uploaded / t_size * 100
            speed = round(uploaded / diff, 2)
            eta = round((t_size - uploaded) / speed)
            progress_str = "`{0}{1} {2}%`".format(
                "".join(["●" for i in range(math.floor(percentage / 5))]),
                "".join(["" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2),
            )
            current_message = (
                f"`✦ Meng-Upload ke G-Drive`\n\n"
                + f"`✦ Nama File:` `{file_name}`\n\n"
                + f"{progress_str}\n\n"
                + f"`✦ Di Upload:` `{humanbytes(uploaded)} of {humanbytes(t_size)}`\n"
                + f"`✦ Kecepatan:` `{humanbytes(speed)}`\n"
                + f"`✦ Perkiraan waktu:` `{time_formatter(eta*1000)}`"
            )
            if display_message != current_message:
                try:
                    await event.edit(current_message)
                    display_message = current_message
                except Exception:
                    pass
    file_id = response.get("id")
    drive_service.permissions().insert(fileId=file_id, body=permissions).execute()
    file = drive_service.files().get(fileId=file_id).execute()
    download_url = file.get("webContentLink")
    return download_url


# Gdrive End


def dani_ck(filroid):
    if os.path.exists(filroid):
        no = 1
        while True:
            ult = "{0}_{2}{1}".format(*os.path.splitext(filroid) + (no,))
            if os.path.exists(ult):
                no += 1
            else:
                return ult
    return filroid


def un_plug(shortname):
    try:
        try:
            for i in LOADED[shortname]:
                king_bot.remove_event_handler(i)
            try:
                del LOADED[shortname]
                del LIST[shortname]
                ADDONS.remove(shortname)
            except BaseException:
                pass

        except BaseException:
            name = f"addons.{shortname}"

            for i in reversed(range(len(king_bot._event_builders))):
                ev, cb = king_bot._event_builders[i]
                if cb.__module__ == name:
                    del king_bot._event_builders[i]
                    try:
                        del LOADED[shortname]
                        del LIST[shortname]
                        ADDONS.remove(shortname)
                    except KeyError:
                        pass
    except BaseException:
        raise ValueError


async def dler(ev, opts, url):
    try:
        await ev.edit("`Mengambil data, harap menunggu..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        return await ev.edit(f"`{str(DE)}`")
    except ContentTooShortError:
        return await ev.edit("`Konten yang di download terlalu pendek.`")
    except GeoRestrictedError:
        return await ev.edit(
            "`Video tidak tersedia pada lokasi anda dikarenakan pembatasan lokasi oleh sebuah website.`",
        )
    except MaxDownloadsReached:
        return await ev.edit("`Download maximal telah tercapai.`")
    except PostProcessingError:
        return await ev.edit("`Ada sebuah error ketika post processing.`")
    except UnavailableVideoError:
        return await ev.edit("`Media tidak tersedia untuk format tersebut.`")
    except XAttrMetadataError as XAME:
        return await ev.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await ev.edit("`Ada sebuah error ketika meng-extract file.`")
    except Exception as e:
        return await ev.edit(f"{str(type(e)): {str(e)}}")
    return ytdl_data


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def progress(current, total, event, start, type_of_ps, file_name=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = round((total - current) / speed) * 1000
        progress_str = "`[{0}{1}] {2}%`\n\n".format(
            "".join(["●" for i in range(math.floor(percentage / 5))]),
            "".join(["" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )
        tmp = (
            progress_str
            + "`{0} of {1}`\n\n`✦ Speed: {2}/s`\n\n`✦ ETA: {3}`\n\n".format(
                humanbytes(current),
                humanbytes(total),
                humanbytes(speed),
                time_formatter(time_to_completion),
            )
        )
        if file_name:
            await event.edit(
                "`✦ {}`\n\n`Nama File: {}`\n\n{}".format(type_of_ps, file_name, tmp)
            )
        else:
            await event.edit("`✦ {}`\n\n{}".format(type_of_ps, tmp))


async def restart(king):
    if Var.HEROKU_APP_NAME and Var.HEROKU_API:
        try:
            Heroku = heroku3.from_key(Var.HEROKU_API)
        except BaseException:
            return await king.edit(
                "`HEROKU_API` salah! Cek kembali di config vars."
            )
        await king.edit("`Memulai ulang kembali, harap tunggu!`")
        app = Heroku.apps()[Var.HEROKU_APP_NAME]
        app.restart()
    else:
        os.execl(executable, executable, "-m", "pyking")


async def shutdown(capt, dynotype=["web", "worker"]):
    capt = await eor(capt, "Mematikan Sistem...")
    if Var.HEROKU_APP_NAME and Var.HEROKU_API:
        try:
            Heroku = heroku3.from_key(Var.HEROKU_API)
        except BaseException:
            return await capt.edit("`HEROKU_API` salah! Silahkan cek kembali di config vars.")
        await capt.edit("`Mematikan aplikasi anda, tunggu beberapa menit!`")
        app = Heroku.apps()[Var.HEROKU_APP_NAME]
        if isinstance(dynotype, list):
            app.process_formation()[(dynotype[0])].scale(0)
            app.process_formation()[(dynotype[1])].scale(0)
        elif isinstance(dynotype, str):
            if dynotype == "userbot":
                dynotype = "worker"
            elif dynotype == "vcbot":
                dynotype = "web"
            else:
                pass
            app.process_formation()[dynotype].scale(0)
        else:
            return
    else:
        sys.exit(0)


async def get_user_info(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Balas pesan user atau berikan id / username.`")
            return None, None
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            return None, None
    return user_obj, extra


def ReTrieveFile(input_file_name):
    RMBG_API = udB.get("RMBG_API")
    headers = {"X-API-Key": RMBG_API}
    files = {"image_file": (input_file_name, open(input_file_name, "rb"))}
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )
    return r


async def resize_photo(photo):
    """ Resize Foto ke 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)
    return image


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = " ".join(names)
    return full_name


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await king_bot(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await king_bot(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await eor(event, "`Grup atau channel invalid.`")
            return None
        except ChannelPrivateError:
            await eor(
                event, "`Ini adalah grup/channel privat atau mungkin saya di ban disana.`"
            )
            return None
        except ChannelPublicGroupNaError:
            await eor(event, "`Channel atau supergroup tidak ditemukan.`")
            return None
        except (TypeError, ValueError) as err:
            await eor(event, str(err))
            return None
    return chat_info


async def fetch_info(chat, event):
    chat_obj_info = await king_bot.get_entity(chat.full_chat.id)
    broadcast = (
        chat_obj_info.broadcast if hasattr(chat_obj_info, "broadcast") else False
    )
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat_obj_info.title
    warn_emoji = emojize(":warning:")
    try:
        msg_info = await king_bot(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=None,
                add_offset=-0,
                limit=0,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as e:
        msg_info = None
        print("Exception:", e)
    first_msg_valid = (
        True
        if msg_info and msg_info.messages and msg_info.messages[0].id == 1
        else False
    )
    creator_valid = True if first_msg_valid and msg_info.users else False
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Deleted Account"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and isinstance(msg_info.messages[0].action, MessageActionChannelMigrateFrom)
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    try:
        dc_id, location = get_input_location(chat.full_chat.chat_photo)
    except Exception as e:
        dc_id = "Unknown"
        str(e)

    description = chat.full_chat.about
    members = (
        chat.full_chat.participants_count
        if hasattr(chat.full_chat, "participants_count")
        else chat_obj_info.participants_count
    )
    admins = (
        chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    )
    banned_users = (
        chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    )
    restrcited_users = (
        chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    )
    members_online = (
        chat.full_chat.online_count if hasattr(chat.full_chat, "online_count") else 0
    )
    group_stickers = (
        chat.full_chat.stickerset.title
        if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = (
        chat.full_chat.read_inbox_max_id
        if hasattr(chat.full_chat, "read_inbox_max_id")
        else None
    )
    messages_sent_alt = (
        chat.full_chat.read_outbox_max_id
        if hasattr(chat.full_chat, "read_outbox_max_id")
        else None
    )
    exp_count = chat.full_chat.pts if hasattr(chat.full_chat, "pts") else None
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info  # this is a list
    bots = 0
    supergroup = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "megagroup") and chat_obj_info.megagroup
        else "No"
    )
    slowmode = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else "No"
    )
    slowmode_time = (
        chat.full_chat.slowmode_seconds
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else None
    )
    restricted = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
        else "No"
    )
    verified = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "verified") and chat_obj_info.verified
        else "No"
    )
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(creator_username) if creator_username else None

    if admins is None:
        try:
            participants_admins = await king_bot(
                GetParticipantsRequest(
                    channel=chat.full_chat.id,
                    filter=ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            print("Exception:", e)
    if bots_list:
        for bot in bots_list:
            bots += 1

    caption = "<b>CHAT INFO:</b>\n"
    caption += f"ID: <code>{chat_obj_info.id}</code>\n"
    if chat_title is not None:
        caption += f"{chat_type} nama: {chat_title}\n"
    if former_title is not None:
        caption += f"Nama Former: {former_title}\n"
    if username is not None:
        caption += f"{chat_type} tipe: Publik\n"
        caption += f"Link: {username}\n"
    else:
        caption += f"{chat_type} tipe: Privat\n"
    if creator_username is not None:
        caption += f"Pembuat: {creator_username}\n"
    elif creator_valid:
        caption += (
            f'Pembuat: <a href="tg://user?id={creator_id}">{creator_firstname}</a>\n'
        )
    if created is not None:
        caption += f"Dibuat: <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"Dibuat: <code>{chat_obj_info.date.date().strftime('%b %d, %Y')} - {chat_obj_info.date.time()}</code> {warn_emoji}\n"
    caption += f"Data Center ID: {dc_id}\n"
    if exp_count is not None:
        chat_level = int((1 + sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"{chat_type} level: <code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"Pesan yang bisa dilihat: <code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"Pesan terkirim: <code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += f"Pesan terkirim: <code>{messages_sent_alt}</code> {warn_emoji}\n"
    if members is not None:
        caption += f"Anggota: <code>{members}</code>\n"
    if admins is not None:
        caption += f"Admin: <code>{admins}</code>\n"
    if bots_list:
        caption += f"Bot: <code>{bots}</code>\n"
    if members_online:
        caption += f"User online: <code>{members_online}</code>\n"
    if restrcited_users is not None:
        caption += f"User dibatasi: <code>{restrcited_users}</code>\n"
    if banned_users is not None:
        caption += f"User ter ban: <code>{banned_users}</code>\n"
    if group_stickers is not None:
        caption += f'{chat_type} stickers: <a href="t.me/addstickers/{chat.full_chat.stickerset.short_name}">{group_stickers}</a>\n'
    caption += "\n"
    if not broadcast:
        caption += f"Slow mode: {slowmode}"
        if (
            hasattr(chat_obj_info, "slowmode_enabled")
            and chat_obj_info.slowmode_enabled
        ):
            caption += f", <code>{slowmode_time}s</code>\n\n"
        else:
            caption += "\n\n"
    if not broadcast:
        caption += f"Supergroup: {supergroup}\n\n"
    if hasattr(chat_obj_info, "restricted"):
        caption += f"Dibatasi: {restricted}\n"
        if chat_obj_info.restricted:
            caption += f"> Platform: {chat_obj_info.restriction_reason[0].platform}\n"
            caption += f"> Alasan: {chat_obj_info.restriction_reason[0].reason}\n"
            caption += f"> Text: {chat_obj_info.restriction_reason[0].text}\n\n"
        else:
            caption += "\n"
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "Scam: <b>Yes</b>\n\n"
    if hasattr(chat_obj_info, "verified"):
        caption += f"Terverifikasi oleh telegram: {verified}\n\n"
    if description:
        caption += f"Deskripsi: \n<code>{description}</code>\n"
    return caption


async def safeinstall(event):
    if event.reply_to_msg_id:
        ok = await eor(event, "`Installing...`")
        try:
            downloaded_file_name = await ok.client.download_media(
                await event.get_reply_message(), "addons/"
            )
            n = event.text
            q = n[9:]
            if q != "f":
                xx = open(downloaded_file_name, "r")
                yy = xx.read()
                xx.close()
                try:
                    for dan in DANGER:
                        if dan in yy:
                            os.remove(downloaded_file_name)
                            return await ok.edit(
                                f"**Instalasi Dibatalkan.**\n**Alasan:** Terjadi sebuah `{dan}` didalam `{downloaded_file_name}`.\n\nJika kamu percaya ke provider tersebut, atau tahu cara menggunakannya, pakai `{HNDLR}install f` untuk force install.",
                            )
                except BaseException:
                    pass
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_addons(shortname.replace(".py", ""))
                try:
                    plug = shortname.replace(".py", "")
                    if plug in HELP:
                        output = "**Plugin** - `{}`\n".format(plug)
                        for i in HELP[plug]:
                            output += i
                        output += "\n© @KingUserbotChannel"
                        await ok.edit(
                            f"✓ `King-Userbot - Installed`: `{plug}` ✓\n\n{output}"
                        )
                        await asyncio.sleep(9)
                        await ok.delete()
                    elif plug in CMD_HELP:
                        kk = f"Nama Plugin-{plug}\n\n✘ Perintah tersedia-\n\n"
                        kk += str(CMD_HELP[plug])
                        await ok.edit(f"✓ `King-Userbot - Terinstall`: `{plug}` ✓\n\n{kk}")
                        await asyncio.sleep(9)
                        await ok.delete()
                    else:
                        try:
                            x = f"Nama Plugin-{plug}\n\n✘ Perintah tersedia-\n\n"
                            for d in LIST[plug]:
                                x += HNDLR + d
                                x += "\n"
                            await ok.edit(
                                f"✓ `King-Userbot - Terinstall`: `{plug}` ✓\n\n`{x}`"
                            )
                            await asyncio.sleep(5)
                            await ok.delete()
                        except BaseException:
                            await ok.edit(f"✓ `King-Userbot - Terinstall`: `{plug}` ✓")
                            await asyncio.sleep(3)
                            await ok.delete()
                except Exception as e:
                    await ok.edit(str(e))
                    pass
            else:
                os.remove(downloaded_file_name)
                await ok.edit("**ERROR**\nPlugin mungkin sudah pernah ter-install.")
                await asyncio.sleep(4)
                await ok.delete()
        except Exception as e:
            await ok.edit("**ERROR\n**" + str(e))
            os.remove(downloaded_file_name)
            await asyncio.sleep(4)
            await ok.delete()
        else:
            await ok.edit(f"Tolong gunakan `{HNDLR}install` dengan cara balas ke file .py .")
            await asyncio.sleep(4)
            await ok.delete()


async def allcmds(event):
    x = str(LIST)
    xx = (
        x.replace(",", "\n")
        .replace("[", """\n """)
        .replace("]", "\n\n")
        .replace("':", """ Plugin\n ✘ Perintah tersedia-""")
        .replace("'", "")
        .replace("{", "")
        .replace("}", "")
    )
    t = telegraph.create_page(title="Semua perintah", content=[f"{xx}"])
    w = t["url"]
    await eod(event, f"Semua perintah King-Userbot : [Klik Disini]({w})", link_preview=False)


def autopicsearch(query):
    query = query.replace(" ", "-")
    link = f"https://unsplash.com/s/photos/{query}"
    extra = requests.get(link)
    res = bs(extra.content, "html.parser", from_encoding="utf-8")
    results = res.find_all("a", "_2Mc8_")
    return results


def returnpage(query):
    query = query.replace(" ", "%20")
    link = f"http://getwallpapers.com/search?term={query}"
    extra = requests.get(link)
    res = bs(extra.content, "html.parser", from_encoding="utf-8")
    results = res.find_all("a", "ui fluid image")
    return results


def animepp(link):
    pc = requests.get(link).text
    f = re.compile("/\w+/full.+.jpg")
    f = f.findall(pc)
    fy = "http://getwallpapers.com" + random.choice(f)
    res = requests.get(fy)
    img = Image.open(io.BytesIO(res.content))
    return img.save("autopic.jpg")


async def randomchannel(tochat, channel, range1, range2, caption=None):
    do = random.randrange(range1, range2)
    async for x in king_bot.iter_messages(channel, add_offset=do, limit=1):
        try:
            if x.media and caption:
                await king_bot.send_file(tochat, file=x, caption=caption)
                return
            await king_bot.send_message(tochat, x)
        except BaseException:
            try:
                await king_bot.send_file(tochat, x)
            except BaseException:
                pass


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


def mediainfo(media):
    if media:
        xx = str((str(media)).split("(", maxsplit=1)[0])
        if xx == "MessageMediaPhoto":
            m = "pic"
        elif xx == "MessageMediaDocument":
            mim = media.document.mime_type
            if mim == "application/x-tgsticker":
                m = "sticker animated"
            elif "image" in mim:
                if mim == "image/webp":
                    m = "sticker"
                elif mim == "image/gif":
                    m = "gif as doc"
                else:
                    m = "pic as doc"
            elif "video" in mim:
                if "DocumentAttributeAnimated" in str(media):
                    m = "gif"
                elif "DocumentAttributeVideo" in str(media):
                    i = str(media.document.attributes[0])
                    if "supports_streaming=True" in i:
                        m = "video"
                    else:
                        m = "video as doc"
                else:
                    m = "video as doc"
            elif "audio" in mim:
                m = "audio"
            else:
                m = "document"
        return m
