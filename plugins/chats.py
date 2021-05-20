"""
✘ Commands Available -

• `{i}delchat`
    Menghapus grup dengan cmd ini.

• `{i}getlink`
    Mendapatkan link grup.

• `{i}create (g|c) <group_name>`
    Membuat grup dengan nama spesifik.
    g - grup
    c - channel
"""

from telethon.errors import ChatAdminRequiredError as NoAdmin
from telethon.tl.functions.channels import CreateChannelRequest, DeleteChannelRequest
from telethon.tl.functions.messages import CreateChatRequest, DeleteChatUserRequest, ExportChatInviteRequest
from pyking import *


@king_cmd(pattern="delchat$", groups_only=True)
async def _(ev):
    if BOT_MODE:
        return await eor(ev, "`Kamu tidak bisa menggunakan perintah ini menggunakan BOT_MODE")
    xx = await eor(ev, "`Memprossess...`")
    try:
        await ev.client(DeleteChannelRequest(ev.chat_id))
    except TypeError:
        return await eod(xx, "`Tidak Bisa menghapus grup ini.`", time=10)
    except NoAdmin:
        return await eod(xx, "`Saya bukanlah admin.`", time=10)
    await ev.client.send_message(Var.LOG_CHANNEL, f"#Dihapus\nMenghapus {ev.chat_id}")


@king_cmd(pattern="getlink$")
async def _(event):
    xx = await eor(event, "`Memprossess...`")
    try:
        r = await event.client(ExportChatInviteRequest(event.chat_id))
    except NoAdmin:
        return await eod(xx, "`Saya bukanlah admin`.", time=10)
    await eor(xx, f"Link Grup: {r.link}")


@king_cmd(pattern="create (g|c)(?: |$(.*)")
async def _(event):
    if BOT_MODE:
        return await eor(event, "`Anda tidak bisa menggunakan perintah ini di BOT_MODE.`")
    tipe = event.pattern_match.group(1)
    nama = event.pattern_match.group(2)
    xx = await eor(event, "`Memprossess...`")
    if tipe == "g":
        try:
            r = await event.client(
                CreateChatRequest(
                    users=["@missrose_bot"],
                    title=nama,
                ),
            )
            cht_id = r.chats[0].id
            await event.client(
                DeleteChatUserRequest(
                    chat_id=cht_id,
                    user_id="@missrose_bot"
                )
            )
            res = await event.client(
                ExportChatInviteRequest(
                    peer=cht_id
                )
            )
            await xx.edit(
                f"[{nama}]({res.link}) Berhasil dibuat!",
                link_preview=False
            )
        except Exception as EXcep:
            await xx.edit(str(EXcep))
    elif tipe == "c":
        try:
            r = await event.client(
                CreateChannelRequest(
                    title=nama,
                    about="Join @KingUserbotSupport",
                    megagroup=False
                )
            )
            cht_id = r.chats[0].id
            res = await event.client(
                ExportChatInviteRequest(
                    peer=cht_id
                )
            )
            await xx.edit(
                f"[{nama}]({res.link}) Berhasil dibuat!",
                link_preview=False
            )
        except Exception as EXcep:
            await xx.edit(str(EXcep))


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
