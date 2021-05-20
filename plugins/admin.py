"""
✘ Perintah Tersedia -

• `{i}promote <balas ke user/userid/username>`
    Promote user menjadi admin dari sebuah chat.

• `{i}demote <balas ke user/userid/username>`
    Melepas jabatan admin dari sebuah chat.

• `{i}ban <balas ke user/userid/username> <alasan>`
    Ban user dari sebuah chat

• `{i}unban <balas ke user/userid/username> <alasan>`
    Unban user dari sebuah chat.

• `{i}kick <balas ke user/userid/username> <alasan>`
    Kick pesan dari sebuah chat.

• `{i}pin <balas ke pesan>`
    Pin pesan di sebuah chat
    Untuk pin yang tidak ada notif, gunakan ({i}pin silent).

• `{i}unpin (all) <balas ke pesan>`
    Unpin pesan di sebuah chat.

• `{i}purge <balas ke pesan>`
    Hapus semua pesan dimulai dari pesan yang dibalas sampai akhir.

• `{i}purgeme <balas ke pesan>`
    Menghapus pesan mu dimulai dari pesan yang dibalas sampai akhir.

• `{i}purgeall <balas ke pesan>`
    Hapus semua pesan pengguna yang di reply.

• `{i}del <balas ke pesan>`
    Hapus pesan yang dibalas.

• `{i}edit <pesan baru>`
    Edit pesan terakhir.
"""
import asyncio

from telethon.errors import UserIdInvalidError, BadRequestError, UserAdminInvalidError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from plugins import OWNER_NAME, OWNER_ID
from pyking import HNDLR, king_bot, HELP
from pyking.dB import DEVLIST
from pyking.functions.all import get_user_info
from pyking.misc._decorators import king_cmd
from pyking.misc._wrappers import eor, eod


@king_cmd(pattern="promote ?(.*)", groups_only=True, admins_only=True)
async def promote(event):
    reps = await eor(event, "`Memproses...`")
    await event.get_chat()
    user, rank = await get_user_info(event)
    if not rank:
        rank = "Admin"
    if not user:
        return await reps.edit("`Balas ke pengguna untuk menjadikannya admin`")
    try:
        await king_bot(
            EditAdminRequest(
                event.chat_id,
                user.id,
                ChatAdminRights(
                    change_info=False,
                    add_admins=False,
                    invite_users=True,
                    manage_call=True,
                    delete_messages=True,
                    pin_messages=True,
                    ban_users=True
                ),
                rank
            )
        )
        await reps.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `"
            f"sekarang adalah admin di {event.chat.title} dengan nama {rank}.`"
        )
    except BadRequestError:
        return await reps.edit("`Aku tidak memiliki izin untuk menjadikanmu admin`")
    await asyncio.sleep(5)
    await reps.delete()


@king_cmd(pattern="demote ?(.*)", groups_only=True, admins_only=True)
async def demote(event):
    reps = await eor(event, "`Memproses...`")
    await event.get_chat()
    user, rank = await get_user_info(event)
    if not rank:
        rank = "Not Admin"
    if not user:
        return await event.edit("`Balas ke pengguna untuk menghapus dia dari admin.`")
    try:
        await king_bot(
            EditAdminRequest(
                event.chat_id,
                user.id,
                ChatAdminRights(
                    change_info=None,
                    manage_call=None,
                    add_admins=None,
                    invite_users=None,
                    ban_users=None,
                    pin_messages=None,
                    delete_messages=None
                ),
                rank
            )
        )
        await reps.edit(
            f"[{user.first_name}](tg://user?id={user.id}) "
            f"`sudah tidak lagi menjadi admin di {event.chat.title}`"
        )
    except BadRequestError:
        return await reps.edit("`Saya tidak memiliki izin untuk menurunkan jabatan admin anda`")
    await asyncio.sleep(5)
    await reps.delete()


@king_cmd(pattern="ban ?(.*)", groups_only=True, admins_only=True)
async def bans(event):
    reps = await eor(event, "`Memproses...`")
    await event.get_chat()
    user, reason = await get_user_info(event)
    if not user:
        return await reps.edit(
            "`Balas pesan ke pengguna atau berikan username untuk melakukan ban`"
        )
    if str(user.id) in DEVLIST:
        return await reps.edit("`Maaf, anda tidak bisa ban pembuat saya.`")
    try:
        await king_bot.edit_permissions(event.chat_id, user.id, view_messages=False)
    except UserAdminInvalidError:
        return await reps.edit("`Saya tidak memiliki izin untuk ban pengguna.`")
    except UserIdInvalidError:
        await reps.edit("`Saya tidak bisa mendapatkan info tentang dia.`")
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await reps.edit(
            f"╔══════════════"
            f"╠ 𝐁𝐚𝐧𝐧𝐞𝐝 𝐔𝐬𝐞𝐫 \n"
            f"╠══════════════"
            f"╠ 𝙽𝚊𝚖𝚊 : [{user.first_name}](tg://user?id={user.id})\n"
            f"╠ 𝙳𝚒 𝙱𝚊𝚗 𝙾𝚕𝚎𝚑 : [{OWNER_NAME}](tg://user?id={OWNER_ID})\n"
            f"╠ 𝙳𝚊𝚕𝚊𝚖 𝙶𝚛𝚞𝚙 : `{event.chat.title}`\n"
            f"╠ 𝙰𝚕𝚊𝚜𝚊𝚗 : `{reason}`\n"
            f"╠ 𝙿𝚎𝚜𝚊𝚗 𝙳𝚒𝚑𝚊𝚙𝚞𝚜 : `Tidak`\n"
            f"╚══════════════"
        )
    if reason:
        await reps.edit(
            f"╔══════════════"
            f"╠ 𝐁𝐚𝐧𝐧𝐞𝐝 𝐔𝐬𝐞𝐫 \n"
            f"╠══════════════"
            f"╠ 𝙽𝚊𝚖𝚊 : [{user.first_name}](tg://user?id={user.id})\n"
            f"╠ 𝙳𝚒 𝙱𝚊𝚗 𝙾𝚕𝚎𝚑 : [{OWNER_NAME}](tg://user?id={OWNER_ID})\n"
            f"╠ 𝙳𝚊𝚕𝚊𝚖 𝙶𝚛𝚞𝚙 : `{event.chat.title}`\n"
            f"╠ 𝙰𝚕𝚊𝚜𝚊𝚗 : `{reason}`\n"
            f"╚══════════════"
        )
    else:
        await reps.edit(
            f"╔══════════════"
            f"╠ 𝐁𝐚𝐧𝐧𝐞𝐝 𝐔𝐬𝐞𝐫 \n"
            f"╠══════════════"
            f"╠ 𝙽𝚊𝚖𝚊 : [{user.first_name}](tg://user?id={user.id})\n"
            f"╠ 𝙳𝚒 𝙱𝚊𝚗 𝙾𝚕𝚎𝚑 : [{OWNER_NAME}](tg://user?id={OWNER_ID})\n"
            f"╠ 𝙳𝚊𝚕𝚊𝚖 𝙶𝚛𝚞𝚙 : `{event.chat.title}`\n"
            f"╚══════════════"
        )


@king_cmd(pattern="unban ?(.*)", groups_only=True, admins_only=True)
async def unbans(event):
    reps = await eor(event, "`Memproses...`")
    await event.get_chat()
    user, reason = await get_user_info(event)
    if not user:
        return await reps.edit("`Balas ke pengguna atau berikan username untuk di unban.`")
    try:
        await king_bot.edit_permissions(event.chat.id, user.id, view_messages=True)
    except UserAdminInvalidError:
        return await reps.edit("`Saya tidak memiliki izin untuk unban pengguna.`")
    except UserIdInvalidError:
        await reps.edit("`Saya tidak bisa mendapatkan info user ini!`")
    if reason:
        await reps.edit(
            f"╔══════════════"
            f"╠ 𝐔𝐧𝐛𝐚𝐧 𝐔𝐬𝐞𝐫 \n"
            f"╠══════════════"
            f"╠ 𝙽𝚊𝚖𝚊 : [{user.first_name}](tg://user?id={user.id})\n"
            f"╠ 𝙳𝚒 𝚄𝚗𝚋𝚊𝚗 𝙾𝚕𝚎𝚑 : [{OWNER_NAME}](tg://user?id={OWNER_ID})\n"
            f"╠ 𝙳𝚊𝚕𝚊𝚖 𝙶𝚛𝚞𝚙 : `{event.chat.title}`\n"
            f"╠ 𝙰𝚕𝚊𝚜𝚊𝚗 : `{reason}`\n"
            f"╚══════════════"
        )
    else:
        await reps.edit(
            f"╔══════════════"
            f"╠ 𝐔𝐧𝐛𝐚𝐧 𝐔𝐬𝐞𝐫 \n"
            f"╠══════════════"
            f"╠ 𝙽𝚊𝚖𝚊 : [{user.first_name}](tg://user?id={user.id})\n"
            f"╠ 𝙳𝚒 𝚄𝚗𝚋𝚊𝚗 𝙾𝚕𝚎𝚑 : [{OWNER_NAME}](tg://user?id={OWNER_ID})\n"
            f"╠ 𝙳𝚊𝚕𝚊𝚖 𝙶𝚛𝚞𝚙 : `{event.chat.title}`\n"
            f"╚══════════════"
        )


@king_cmd(
    pattern="kick ?(.*)",
    groups_only=True,
    admins_only=True
)
async def kick(event):
    if event.text == f"{HNDLR}kickme":
        return
    reps = await eor(event, "`Memproses...`")
    await event.get_chat()
    user, reason = await get_user_info(event)
    if not user:
        return await reps.edit(
            "`Balas pesan ke pengguna atau berikan username untuk melakukan kick`"
        )
    if str(user.id) in DEVLIST:
        return await reps.edit("`Maaf, anda tidak bisa kick pembuat saya.`")
    if user.id == king_bot.uid:
        return await reps.edit("`Anda tidak bisa kick diri sendiri.`")
    try:
        await king_bot.kick_participant(event.chat_id, user.id)
        await asyncio.sleep(0.5)
    except BadRequestError:
        return await reps.edit("`Saya tidak memiliki izin untuk kick pengguna.`")
    except Exception as Ex:
        return await reps.edit(
            f"`Saya tidak memiliki izin untuk kick pengguna.`\n\n**ERROR**:\n`{str(Ex)}`"
        )
    if reason:
        await reps.edit(
            f"╔══════════════"
            f"╠ 𝐊𝐢𝐜𝐤𝐞𝐝 𝐔𝐬𝐞𝐫 \n"
            f"╠══════════════"
            f"╠ 𝙽𝚊𝚖𝚊 : [{user.first_name}](tg://user?id={user.id})\n"
            f"╠ 𝙳𝚒 𝙺𝚒𝚌𝚔 𝙾𝚕𝚎𝚑 : [{OWNER_NAME}](tg://user?id={OWNER_ID})\n"
            f"╠ 𝙳𝚊𝚕𝚊𝚖 𝙶𝚛𝚞𝚙 : `{event.chat.title}`\n"
            f"╠ 𝙰𝚕𝚊𝚜𝚊𝚗 : `{reason}`\n"
            f"╚══════════════"
        )
    else:
        await reps.edit(
            f"╔══════════════"
            f"╠ 𝐊𝐢𝐜𝐤𝐞𝐝 𝐔𝐬𝐞𝐫 \n"
            f"╠══════════════"
            f"╠ 𝙽𝚊𝚖𝚊 : [{user.first_name}](tg://user?id={user.id})\n"
            f"╠ 𝙳𝚒 𝙺𝚒𝚌𝚔 𝙾𝚕𝚎𝚑 : [{OWNER_NAME}](tg://user?id={OWNER_ID})\n"
            f"╠ 𝙳𝚊𝚕𝚊𝚖 𝙶𝚛𝚞𝚙 : `{event.chat.title}`\n"
            f"╚══════════════"
        )


@king_cmd(pattern="pin ?(.*)")
async def pin(event):
    if not event.is_private:
        await event.get_chat()
    chat = await king_bot.get_entity(event.chat_id)
    repl = event.reply_to_msg_id
    txt = event.text
    reps = await eor(event, "`Memproses...`")
    try:
        kk = txt[4]
        if kk:
            return
    except BaseException as BE:
        return BE
    if not event.is_reply:
        await reps.edit("`Balas ke sebuah pesan untuk mem-pin pesan.`")
    ch = event.pattern_match.group(1)
    if ch != "silent":
        slnt = True
        try:
            await king_bot.pin_message(event.chat_id, repl, notify=slnt)
        except BadRequestError:
            return await reps.edit("`Saya tidak memiliki izin untuk melakukan ini.`")
        except Exception as Ex:
            return await reps.edit(f"**ERROR** : {str(Ex)}")
        await reps.edit(
            f"╔═══════════════"
            f"╠ 𝐏𝐢𝐧𝐧𝐞𝐝 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 \n"
            f"╠═══════════════"
            f"╠ 𝙿𝚎𝚜𝚊𝚗 : [𝙿𝚎𝚜𝚊𝚗](https://t.me/c/{chat.id}/{repl})\n"
            f"╚══════════════"
        )
    else:
        try:
            await king_bot.pin_message(event.chat_id, repl, notify=False)
        except BadRequestError:
            return await reps.edit("`Saya tidak memiliki izin untuk melakukan ini.`")
        except Exception as Ex:
            return await reps.edit(f"**ERROR** : {str(Ex)}")
        try:
            await event.delete()
        except BaseException as BE:
            return BE


@king_cmd(
    pattern="unpin($| (.*)"
)
async def unpin(event):
    reps = await eor(event, "`Memproses...`")
    if not event.is_private:
        await event.get_chat()
    ch = (event.pattern_match.group(1)).strip()
    msg = event.reply_to_msg_id
    if msg and not ch:
        try:
            await king_bot.unpin_message(event.chat_id, msg)
        except BadRequestError:
            return await reps.edit("`Saya tidak memiliki izin untuk melakukan ini.`")
        except Exception as Ex:
            return await reps.edit(f"**ERROR** : {str(Ex)}")
    elif ch == "all":
        try:
            await king_bot.unpin_message(event.chat_id)
        except BadRequestError:
            return await reps.edit(
                "`Saya tidak memiliki izin untuk melakukan ini.`"
            )
        except Exception as Ex:
            return await reps.edit(f"**ERROR** : {str(Ex)}")
    else:
        return await reps.edit(
            f"Balas sebuah pesan atau gunakan `{HNDLR}unpin all` untuk unpin semua pesan"
        )
    if not msg and ch != "all":
        return await reps.edit(
            f"Balas sebuah pesan atau gunakan `{HNDLR}unpin all` untuk unpin semua pesan"
        )
    await reps.edit("𝐏𝐞𝐬𝐚𝐧 𝐝𝐢 𝐔𝐧𝐩𝐢𝐧!")


@king_cmd(pattern="purge$")
async def purger(event):
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    if not event.reply_to_msg_id:
        return await eod(event, "`Balas ke sebuah pesan untuk memulai penghapusan.`", time=10)
    async for msg in king_bot.iter_messages(chat, min_id=event.reply_to_msg_id):
        msgs.append(msg)
        count += 1
        msgs.append(event.reply_to_msg_id)
        if len(msgs) == 100:
            await king_bot.delete_messages(chat, msgs)
            msgs = []
    if msgs:
        await king_bot.delete_messages(chat, msgs)
    done = await king_bot.send_message(
        event.chat_id,
        f"__Hapus Pesan Sebanyak {str(count)} Sukses!__"
    )
    await asyncio.sleep(5)
    await done.delete()


@king_cmd(pattern="purgeme$")
async def purgeme(event):
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    if not event.reply_to_msg_id:
        return await eod(event, "`Balas ke sebuah pesan untuk memulai penghapusan.`", time=10)
    async for msg in king_bot.iter_messages(
        chat,
        from_user="me",
        min_id=event.reply_to_msg_id
    ):
        msgs.append(msg)
        count += 1
        msgs.append(event.reply_to_msg_id)
        if len(msgs) == 100:
            await king_bot.delete_messages(chat, msgs)
            msgs = []
    if msgs:
        await king_bot.delete_messages(chat, msgs)
    done = await king_bot.send_message(
        event.chat_id,
        f"__Hapus Pesan Sebanyak {str(count)} Sukses!__"
    )
    await asyncio.sleep(5)
    await done.delete()


@king_cmd(pattern="purgeall$")
async def _(event):
    reps = await eor(event, "`Memproses...`")
    if event.reply_to_msg_id:
        sender = (await event.get_reply_message()).sender_id
        name = (await event.client.get_entity(sender)).first_name
        try:
            num = 0
            async for x in king_bot.iter_messages(event.chat_id, from_user=sender):
                await king_bot.delete_messages(event.chat.id, x)
                num += 1
            await reps.edit(
                f"**Menghapus pesan [{name}](tg://user?id={sender}) sebanyak {num} pesan"
            )
        except ValueError as er:
            return await eod(reps, str(er), time=5)
    else:
        return await eod(reps, "`Balas ke sebuah pesan untuk menghapusnya.`", time=5)


@king_cmd(pattern="del$")
async def dels(event):
    reps = await eor(event, "`Memproses...`")
    src = await event.get_reply_message()
    if event.reply_to_msg_id:
        try:
            await src.delete()
            await event.delet()
        except BaseException as BE:
            await eod(
                event,
                f"`Tidak bisa menghapus pesan.`\n\n**ERROR:**\n`{str(BE)}`",
                time=5
            )
    else:
        return await eod(reps, "`Balas ke sebuah pesan untuk menghapusnya.`")


@king_cmd(pattern="edit")
async def editer(event):
    msg = event.text
    chat = await event.get_input_chat()
    self_id = await king_bot.get_peer_id("me")
    string = str(msg[6:])
    i = 1
    async for mess in king_bot.iter_messages(chat, self_id):
        if i == 2:
            await mess.edit(string)
            await event.delete()
            break
        i += 1


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
