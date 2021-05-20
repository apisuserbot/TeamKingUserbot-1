"""
✘ Perintah Tersedia

• `{i}alive`
    Cek jika bot kamu bekerja.

• `{i}ping`
    Cek waktu bot merespon.

• `{i}cmds`
    Melihat semua plugin.

• `{i}restart`
    Memulai ulang bot.

• `{i}shutdown`
    Matikan dyno heroku.
"""

from plugins import *
from pyking import __version__ as KingVer
from telethon import __version__
from telethon.errors import ChatSendMediaForbiddenError
from platform import python_version as pyver
from pyking import *
from pyking.misc._decorators import king_cmd

HEROKU_API = None
HEROKU_APP_NAME = None

try:
    if Var.HEROKU_API and Var.HEROKU_APP_NAME:
        HEROKU_API = Var.HEROKU_API
        HEROKU_APP_NAME = Var.HEROKU_APP_NAME
        Heroku = heroku3.from_key(Var.HEROKU_API)
        heroku_api = "https://api.heroku.com"
        app = Heroku.app(Var.HEROKU_APP_NAME)
except BaseException:
    HEROKU_API = None
    HEROKU_APP_NAME = None


@king_cmd(pattern="alive$", allow_sudo=False)
async def alive(event):
    pic = udB.get("ALIVE_PIC")
    uptime = grt(time.time() - start_time)
    header = udB.get("ALIVE_TEXT") if udB.get("ALIVE_TEXT") else "Hello King!"
    branchs = Repo().active_branch
    remote = Repo().remotes[0].config_reader.get("url")
    reps = remote.replace(".git", f"/tree/{branchs}")
    links = f"[{branchs}]({reps})"
    alv = f"""
    **{header}**
    ┏━━━━━━━━━━━━━━━━━━━━━\n
    ┣ **Pemilik** - `{OWNER_NAME}`\n
    ┣ **Versi** - `{king_version}`\n
    ┣ **Versi Library** - `{KingVer}`\n
    ┣ **UpTime** - `{uptime}`\n
    ┣ **Python** - `{pyver()}`\n
    ┣ **Telethon** - `{__version__}`\n
    ┣ **Branch** - `{links}`\n
    ┗━━━━━━━━━━━━━━━━━━━━━"""
    if pic is None:
        return await eor(event, alv)
    elif pic is not None and "telegra" in pic:
        try:
            await king_bot.send_message(
                event, alv, file=pic, link_preview=False
            )
            await event.delete()
        except ChatSendMediaForbiddenError:
            await eor(event, alv, link_preview=False)
    else:
        try:
            await king_bot.send_message(event.chat_id, file=pic)
            await king_bot.send_message(event.chat_id, alv, link_preview=False)
            await event.delete()
        except ChatSendMediaForbiddenError:
            await eor(event, alv, link_preview=False)


@king_cmd(pattern="ping$")
async def _(event):
    start = datetime.now()
    x = await eor(event, "`Pong!`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    uptime = grt(time.time() - start_time)
    await x.edit(f"**Pong !!** {ms} ms\nBerjalan {uptime}")


@king_cmd(pattern="cmds$")
async def cmds(event):
    await allcmds(event)


@king_cmd(pattern="restart$")
async def _(event):
    if Var.HEROKU_API:
        await eor(event, "`Merestart...`")
        try:
            await restart(event)
        except BaseException:
            await bash("pkill python3 && python3 -m pyking")
    else:
        await bash("pkill python3 && python3 -m pyking")


@king_cmd(pattern="shutdown")
async def _(event):
    try:
        dyno = event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        dyno = None
    if dyno:
        if dyno not in ["userbot", "vcbot", "web", "worker"]:
            await eor(event, "`Tipe dino yang dipilih salah!`")
            return
        await shutdown(event, dyno)
    else:
        await shutdown(event)


@king_cmd(pattern="logs")
async def _(event):
    xx = await eor(event, "`Memprosses...`")
    with open("ultroid.log") as f:
        k = f.read()
    key = (
        requests.post("https://nekobin.com/api/documents", json={"content": k})
        .json()
        .get("result")
        .get("key")
    )
    url = f"https://nekobin.com/{key}"
    await king_bot.send_file(
        event.chat_id,
        file="ultroid.log",
        caption=f"**Logs King Userbot.**\nBisa di klik [disini]({url}) juga"
    )
    await xx.edit("`Selesai!`")
    await xx.delete()


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})