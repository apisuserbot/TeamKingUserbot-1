"""
✘ Commands Available -

• `{i}install <reply to plugin>`
    Meng-Install Plugin,
   `{i}install f`
    Untuk install paksa.

• `{i}uninstall <plugin name>`
    Menghapus plugin.

• `{i}load <plugin name>`
    Memuat plugin.

• `{i}unload <plugin name>`
    Menghapus plugin.

• `{i}help <plugin name>`
    Memunculkan menu help.
"""

from pyking import *
from pyking.misc import in_pattern


@in_pattern(
    "send ?(.*)"
)
@in_owner
async def _(event):
    builder = event.builder
    input_str = event.pattern_match.group(1)
    if input_str is None or input_str == "":
        plugs = await event.builder.article(
            title=f"Plugin yang mana?",
            text="Tidak ada plugin",
            buttons=[[
                Button.switch_inline(
                    "Cari lagi?",
                    query="send ",
                    same_peer=True
                )
            ]]
        )
        await event.answer(plugs)
    else:
        try:
            builders = builder.document(
                f"plugins/{input_str}.py",
                title=f"{input_str}.py",
                description=f"Plugin {input_str} Ditemukan",
                text=f"{input_str}.py gunakan tombol ini untuk dikirim ke neko dan raw..",
                buttons=[
                    [
                        Button.switch_inline(
                            "Cari lagi?",
                            query="send ",
                            same_peer=True
                        )
                    ],
                    [Button.inline("Paste?", data=f"pasta-plugins/{input_str}.py")]
                ]
            )
            return await event.answer([builders])
        except BaseException:
            buildcode = builder.article(
                title=f"Module {input_str}.py tidak ditemukan.",
                description="Tidak ada module",
                text=f"Tidak ada module bernama {input_str}.py",
                buttons=[
                    [
                        Button.switch_inline(
                            "Cari lagi",
                            query="send ",
                            same_peer=True
                        )
                    ]
                ]
            )
            return await event.answer([buildcode])


@king_cmd(pattern=r"load ?(.*)")
async def _(event):
    shortname = event.pattern_match.group(1)
    if not shortname:
        await eor(event, "`Berikan nama plugin untuk dimuat kembali`")
        return
    try:
        try:
            un_plug(shortname)
        except BaseException:
            pass
        load_addons(shortname)
        await eod(event, f"**Sukses memuat plugin** `{shortname}`", time=3)
    except Exception as e:
        await eod(
            event,
            f"**Tidak bisa memuat** `{shortname}` **karena mendapatkan error.**\n`{str(e)}`",
            time=3,
        )


@king_cmd(pattern=r"unload ?(.*)")
async def _(event):
    opt = event.pattern_match.group(1)
    if not opt:
        return await eor(event, "`Berikan nama plugin yang anda inginkan untuk dihapus.`")
    lsdr = os.listdir("addons")
    lstr = os.listdir("plugins")
    pynames = f"{opt}.py"
    if pynames in lsdr:
        try:
            un_plug(opt)
            return await eod(event, f"**Plugin** `{opt}` **Berhasil dihapus.**", time=3)
        except Exception as Ex:
            return await eor(event, str(Ex))
    elif pynames in lstr:
        return await eod(event, "**Kamu tidak bisa menghapus plugin official.**", time=3)
    else:
        return await eod(event, f"**Tidak ada plugin bernama** `{opt}`", time=3)


@king_cmd(pattern=r"uninstall ?(.*)")
async def _(event):
    opt = event.pattern_match.group(1)
    if not opt:
        return await eor(event, "`Berikan nama plugin yang anda inginkan untuk dihapus.`")
    lsdr = os.listdir("addons")
    lstr = os.listdir("plugins")
    pynames = f"{opt}.py"
    if pynames in lsdr:
        try:
            un_plug(opt)
            await eod(event, f"**Plugin** `{opt}` **Berhasil dihapus.**", time=3)
            os.remove(f"addons/{opt}.py")
        except Exception as Ex:
            return await eor(event, str(Ex))
    elif pynames in lstr:
        return await eod(event, "**Kamu tidak bisa menghapus plugin official.**", time=3)
    else:
        return await eod(event, f"**Tidak ada plugin bernama** `{opt}`", time=3)


@king_cmd(pattern="install")
async def _(event):
    if not is_fullsudo(event.sender_id):
        return await eod(event, "`Perintah ini hanya untuk owner.`")
    await safeinstall(event)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
