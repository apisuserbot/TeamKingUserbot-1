# King - UserBot
# Copyright (C) 2020 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.

import re
from math import ceil
from platform import python_version as pyver

from redis import Redis
from telethon import __version__
from telethon.tl.types import InputWebDocument

from pyking import *
from pyking import __version__ as KingVer
from pyking.__main__ import asst
from pyking.misc._assistant import callback, owner, inline, in_owner, in_pattern
from pyking.misc._decorators import sed
from strings import get_string
from . import *

# ================================================#
notmine = f"Bot ini hanya untuk {OWNER_NAME}"
BOT_PIC = "https://telegra.ph/file/1496ffecb9d6422e2ffd0.jpg"
helps = get_string("inline_1")

add_ons = udB.get("ADDONS")
if add_ons:
    zhelps = get_string("inline_2")
else:
    zhelps = get_string("inline_3")
# ================================================#


@in_pattern("")
@in_owner
async def e(o):
    if len(o.text) == 0:
        b = o.builder
        uptime = grt(time.time() - start_time)
        header = udB.get("ALIVE_TEXT") if udB.get("ALIVE_TEXT") else "Hallo, Saya hidup."
        ALIVEMSG = (
            "**{}**\n\n"
            "┏━━━━━━━━━━━━━━━━━━━━━\n"
            "┣ **Pemilik** - `{}`\n"
            "┣ **Versi** - `{}`\n"
            "┣ **Versi pyking** - `{}`\n"
            "┣ **UpTime** - `{}`\n"
            "┣ **Python** - `{}`\n"
            "┣ **Telethon** - `{}`\n"
            "┣ **Branch** - `{}`\n"
            "┗━━━━━━━━━━━━━━━━━━━━━"
        ).format(
            header,
            OWNER_NAME,
            king_version,
            KingVer,
            uptime,
            pyver(),
            __version__,
            Repo().active_branch,
        )
        ress = [
            await b.article(
                title="King-Userbot",
                url="https://t.me/TeamKingUserbot",
                description="Userbot | Telethon ",
                text=ALIVEMSG,
                thumb=InputWebDocument(BOT_PIC, 0, "image/jpeg", []),
                buttons=[
                    [Button.url(text="Grup Support", url="t.me/KingUserbotSupport")],
                    [Button.url(text="Repository", url="https://github.com")],
                ]
            )
        ]
        await o.answer(ress, switch_pm=f"KingUserbot Portal", switch_pm_param="start")


if asst.me is not None:

    @inline
    @in_owner
    async def inline_handler(event):
        builder = event.builder
        query = event.text
        if event.query.user_id in sed and query.startswith("kingd"):
            z = []
            for x in LIST.values():
                for y in x:
                    z.append(y)
            cmd = len(z) + 10
            bnn = await asst.get_me()
            bnn = bnn.username
            result = builder.article(
                title="Menu Help",
                description="Menu Help - Userbot | Telethon ",
                url="https://t.me/TeamKingUserbot",
                thumb=InputWebDocument(BOT_PIC, 0, "image/jpeg", []),
                text=(
                    f"╔=**OWNER** {OWNER_NAME}\n\n"
                    f"╠=**Main Menu**\n\n"
                    f"╠=**Plugin - {len(PLUGINS) - 5}**\n"
                    f"╠=**Custom Plugin - {len(ADDONS)}**\n"
                    f"╚=**Total Perintah{cmd}**\n",
                ),
                buttons=[
                    [
                        Button.inline("• Pʟᴜɢɪɴ", data="plug_data"),
                        Button.inline("• Aᴅᴅᴏɴ", data="addons_data"),
                    ],
                    [
                        Button.inline("Oᴡɴᴇʀ•Tᴏᴏʟ", data="ownr_tools"),
                        Button.inline("Iɴʟɪɴᴇ•Pʟᴜɢɪɴ", data="inline_tools"),
                    ],
                    [
                        Button.url("Sᴇᴛᴛɪɴɢ𝚜", url=f"https://t.me/{bnn}?start=set"),
                    ],
                    [
                        Button.inline("Cʟᴏ𝚜ᴇ", data="close")
                    ],
                ],
            )
            await event.answer([result] if result else None)
        elif event.query.user_id in sed and query.startswith("paste"):
            ok = query.split("-")[1]
            link = f"https://nekobin.com/{ok}"
            link_raw = f"https://nekobin.com/raw/{ok}"
            result = builder.article(
                title="Paste",
                text="Pᴀsᴛᴇᴅ Tᴏ Nᴇᴋᴏʙɪɴ!",
                buttons=[
                    [
                        Button.url("NekoBin", url=f"{link}"),
                        Button.url("Raw", url=f"{link_raw}"),
                    ],
                ],
            )
            await event.answer([result] if result else None)

    @callback("plug_data")
    @owner
    async def on_plug_in_callback_query_handler(event):
        xhelps = helps.format(OWNER_NAME, len(PLUGINS) - 5)
        buttons = paginate_help(0, PLUGINS, "helpme")
        await event.edit(f"{xhelps}", buttons=buttons, link_preview=False)

    @callback("addons_data")
    @owner
    async def addon(event):
        halp = zhelps.format(OWNER_NAME, len(ADDONS))
        if len(ADDONS) > 0:
            buttons = paginate_addon(0, ADDONS, "addon")
            await event.edit(f"{halp}", buttons=buttons, link_previw=False)
        else:
            await event.answer(
                f"• Ketik `{HNDLR}setredis ADDONS True`\nUntuk mendapatkan plugin tambahan",
                cache_time=0,
                alert=True,
            )

    # OWNER TOOLS CALLBACK
    @callback("ownr_tools")
    @owner
    async def setting(event):
        await event.edit(
            buttons=[
                [
                    Button.inline("•Pɪɴɢ•", data="ping_data"),
                    Button.inline("•Wᴀᴋᴛᴜ Aᴋᴛɪꜰ•", data="up_data")
                ],
                [
                    Button.inline("•Rᴇsᴛᴀʀᴛ•", data="rstrt")
                ],
                [
                    Button.inline("←- Kᴇᴍʙᴀʟɪ", data="open")
                ]
            ]
        )

    # SETTING CALLBACK OWNER TOOLS
    @callback("ping_data")
    @owner
    async def _(event):
        start = datetime.now()
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        pin = f"🌋Pɪɴɢ = {ms}ms"
        if event.query.user_id in sed:
            await event.answer(pin, cache_time=0, alert=True)
        else:
            await event.answer(notmine, cache_time=0, alert=True)

    @callback("up_data")
    async def _(event):
        uptime = grt(time.time() - start_time)
        pin = f"🙋Wᴀᴋᴛᴜ Aᴋᴛɪꜰ = {uptime}"
        if event.query.user_id in sed:
            await event.answer(pin, cache_time=0, alert=True)
        else:
            await event.answer(notmine, cache_time=0, alert=True)

    @callback("rstrt")
    async def rrst(event):
        if event.query.user_id in sed:
            await restart(event)
        else:
            await event.answer(notmine, cache_time=0, alert=True)

    # END OF OWNER TOOLS CALLBACK SETTING

    # INLINE TOOLS
    @callback("inline_tools")
    @owner
    async def _(e):
        button = [
            [
                Button.switch_inline(
                    "Kɪʀɪᴍ Pʟᴜɢɪɴ Oꜰꜰɪᴄɪᴀʟ",
                    query="send",
                    same_peer=True
                ),
            ],
            [
                Button.switch_inline(
                    "YᴏᴜTᴜʙᴇ Dᴏᴡɴʟᴏᴀᴅᴇʀ",
                    query="yt dj diam diam menyukaiku",
                    same_peer=True
                )
            ],
            [
                Button.inline(
                    "<- Kᴇᴍʙᴀʟɪ",
                    data="open",
                )
            ],
        ]
        await e.edit(buttons=button, link_preview=False)

    @callback(re.compile(rb"helpme_next\((.+?)\)"))
    @owner
    async def on_plug_in_callback_query_handler(event):
        current_page_number = int(event.data_match.group(1).decode("UTF-8"))
        buttons = paginate_help(current_page_number + 1, PLUGINS, "helpme")
        await event.edit(buttons=buttons, link_preview=False)


    @callback(re.compile(rb"helpme_prev\((.+?)\)"))
    @owner
    async def on_plug_in_callback_query_handler(event):
        current_page_number = int(event.data_match.group(1).decode("UTF-8"))
        buttons = paginate_help(current_page_number - 1, PLUGINS, "helpme")
        await event.edit(buttons=buttons, link_preview=False)


    @callback(re.compile(rb"addon_next\((.+?)\)"))
    @owner
    async def on_plug_in_callback_query_handler(event):
        current_page_number = int(event.data_match.group(1).decode("UTF-8"))
        buttons = paginate_addon(current_page_number + 1, ADDONS, "addon")
        await event.edit(buttons=buttons, link_preview=False)


    @callback(re.compile(rb"addon_prev\((.+?)\)"))
    @owner
    async def on_plug_in_callback_query_handler(event):
        current_page_number = int(event.data_match.group(1).decode("UTF-8"))
        buttons = paginate_addon(current_page_number - 1, ADDONS, "addon")
        await event.edit(buttons=buttons, link_preview=False)


    @callback("back")
    @owner
    async def backr(event):
        xhelps = helps.format(OWNER_NAME, len(PLUGINS) - 5)
        current_page_number = int(upage)
        buttons = paginate_help(current_page_number, PLUGINS, "helpme")
        await event.edit(f"{xhelps}", buttons=buttons, link_preview=False)


    @callback("buck")
    @owner
    async def backr(event):
        xhelps = zhelps.format(OWNER_NAME, len(ADDONS))
        current_page_number = int(addpage)
        buttons = paginate_addon(current_page_number, ADDONS, "addon")
        await event.edit(f"{xhelps}", buttons=buttons, link_preview=False)

    @callback("open")
    @owner
    async def opner(event):
        bnn = asst.me.username
        buttons = [
            [
                Button.inline("• Pʟᴜɢɪɴ𝚜", data="plug_data"),
                Button.inline("• Aᴅᴅᴏɴ𝚜", data="addons_data"),
            ],
            [
                Button.inline("Oᴡɴᴇʀ•Tᴏᴏʟ𝚜", data="ownr_tools"),
                Button.inline("Iɴʟɪɴᴇ•Pʟᴜɢɪɴ𝚜", data="inline_tools"),
            ],
            [
                Button.url("Sᴇᴛᴛɪɴɢ𝚜", url=f"https://t.me/{bnn}?start={king_bot.me.id}"),
            ],
            [
                Button.inline("Cʟᴏ𝚜ᴇ", data="close")
            ],
        ]
        z = []
        for x in LIST.values():
            for y in x:
                z.append(y)
        cmd = len(z) + 10
        await event.edit(
            f"╔OWNER {OWNER_NAME}\n\n"
            f"╠=**Main Menu**\n\n"
            f"╠=**Plugin - {len(PLUGINS) - 5}**\n"
            f"╠=**Custom Plugin - {len(ADDONS)}**\n"
            f"╚=**Total Perintah{cmd}**\n",
            buttons=buttons,
            link_preview=False,
        )

    @callback("close")
    @owner
    async def on_plug_in_callback_query_handler(event):
        await event.edit(
            "`Menu Telah Ditutup.`",
            buttons=Button.inline("Bᴜᴋᴀ Mᴀɪɴ Mᴇɴᴜ Kᴇᴍʙᴀʟɪ", data="open"),
        )

    @callback(
        re.compile(
            b"us_plugin_(.*)",
        ),
    )
    @owner
    async def on_plug_in_callback_query_handler(event):
        plugin_name = event.data_match.group(1).decode("UTF-8")
        help_string = f"Nama Plugin - `{plugin_name}`\n"
        try:
            for i in HELP[plugin_name]:
                help_string += i
        except BaseException:
            pass
        if help_string == "":
            reply_pop_up_alert = f"{plugin_name} tidak memiliki bantuan detail..."
        else:
            reply_pop_up_alert = help_string
        reply_pop_up_alert += "\n© @TeamKingUserbot"
        try:
            if event.query.user_id in sed:
                await event.edit(
                    reply_pop_up_alert,
                    buttons=[
                        Button.inline("<- Kᴇᴍʙᴀʟɪ", data="back"),
                        Button.inline("••Tᴜᴛᴜᴘ••", data="close"),
                    ],
                )
            else:
                reply_pop_up_alert = notmine
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        except BaseException:
            halps = f"Gunakan .help {plugin_name} untuk mendapatkan daftar perintah."
            await event.edit(halps)


    @callback(
        re.compile(
            b"add_plugin_(.*)",
        ),
    )
    @owner
    async def on_plug_in_callback_query_handler(event):
        plugin_name = event.data_match.group(1).decode("UTF-8")
        help_string = ""
        try:
            for i in HELP[plugin_name]:
                help_string += i
        except BaseException:
            try:
                for _ in CMD_HELP[plugin_name]:
                    help_string = (
                        f"Nama Plugin-{plugin_name}\n\n✘ Perintah Tersedia-\n\n"
                    )
                    help_string += str(CMD_HELP[plugin_name])
            except BaseException:
                try:
                    if plugin_name in LIST:
                        help_string = (
                            f"Nama Plugin-{plugin_name}\n\n✘ Perintah Tersedia-\n\n"
                        )
                        for d in LIST[plugin_name]:
                            help_string += HNDLR + d
                            help_string += "\n"
                except BaseException:
                    pass
        if help_string == "":
            reply_pop_up_alert = f"{plugin_name} tidak memiliki bantuan detail..."
        else:
            reply_pop_up_alert = help_string
        reply_pop_up_alert += "\n© @TeamKingUserbot"
        try:
            if event.query.user_id in sed:
                await event.edit(
                    reply_pop_up_alert,
                    buttons=[
                        Button.inline("<- Kᴇᴍʙᴀʟɪ", data="buck"),
                        Button.inline("••Tᴜᴛᴜᴘ••", data="close"),
                    ],
                )
            else:
                reply_pop_up_alert = notmine
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        except BaseException:
            halps = f"Lakukan .help {plugin_name} untuk mendapatkan daftar perintah."
            await event.edit(halps)


def paginate_help(page_number, loaded_plugins, prefix):
    number_of_rows = 5
    number_of_cols = 2
    emoji = Redis("EMOJI_IN_HELP")
    if emoji:
        multi, mult2i = emoji, emoji
    else:
        multi, mult2i = "✘", "✘"
    helpable_plugins = []
    global upage
    upage = page_number
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        Button.inline(
            "{} {} {}".format(
                random.choice(list(multi)),
                x,
                random.choice(list(mult2i)),
            ),
            data=f"us_plugin_{x}",
        )
        for x in helpable_plugins
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                Button.inline(
                    "<- Sᴇʙᴇʟᴜᴍɴʏᴀ",
                    data=f"{prefix}_prev({modulo_page})",
                ),
                Button.inline("-Kᴇᴍʙᴀʟɪ-", data="open"),
                Button.inline(
                    "Sᴇʟᴀɴᴊᴜᴛɴʏᴀ ->",
                    data=f"{prefix}_next({modulo_page})",
                ),
            ),
        ]
    else:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [(Button.inline("-Kᴇᴍʙᴀʟɪ-", data="open"),)]
    return pairs


def paginate_addon(page_number, loaded_plugins, prefix):
    number_of_rows = 5
    number_of_cols = 2
    emoji = Redis("EMOJI_IN_HELP")
    if emoji:
        multi, mult2i = emoji, emoji
    else:
        multi, mult2i = "✘", "✘"
    helpable_plugins = []
    global addpage
    addpage = page_number
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        Button.inline(
            "{} {} {}".format(
                random.choice(list(multi)),
                x,
                random.choice(list(mult2i)),
            ),
            data=f"add_plugin_{x}",
        )
        for x in helpable_plugins
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                Button.inline(
                    "<- Sᴇʙᴇʟᴜᴍɴʏᴀ",
                    data=f"{prefix}_prev({modulo_page})",
                ),
                Button.inline("-Kᴇᴍʙᴀʟɪ-", data="open"),
                Button.inline(
                    "Sᴇʟᴀɴᴊᴜᴛɴʏᴀ ->",
                    data=f"{prefix}_next({modulo_page})",
                ),
            ),
        ]
    else:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [(Button.inline("-Kᴇᴍʙᴀʟɪ-", data="open"),)]
    return pairs
