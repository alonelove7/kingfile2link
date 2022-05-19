# (c) adarsh-goel 
from Adarsh.bot import StreamBot
from Adarsh.vars import Var
import logging
logger = logging.getLogger(__name__)
from Adarsh.bot.plugins.stream import MY_PASS
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)
from pyrogram.types import ReplyKeyboardMarkup

                      
@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"🔆اطلاعیه\n\n🔰کاربر [{m.from_user.first_name}](tg://user?id={m.from_user.id}) وارد ربات شد."
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL is not None:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "banned":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="⛔️حساب کاربری شما به دلیل تخلف مسدود شده است⛔️",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="📛 برای حمایت از ما و همچنان ربات ابتدا در کانال ما عضو شوید.\n\n✅ پس از عضویت وارد ربات شده و دستور /start را ارسال کنید.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("💠عضویت در کانال💠", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="*",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text="⚡️خوش آمدید\n\n💥برای استفاده از ربات کافی است فایل خود را ارسال کرده و سپس لینک آن را دریافت کنید.\n\n🆔 @King_Network7",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("کانال ربات⚜️", url="https://t.me/king_network7"), InlineKeyboardButton("💰دونیت", url="https://www.payping.ir/d/WiZG")],
                    [InlineKeyboardButton("ربات SMS بمبر🌀", url="https://t.me/King_Spam_bot"), InlineKeyboardButton("🌀ربات لینک به فایل", url="https://t.me/King7Up2roBot")],
                ]
            ),
            disable_web_page_preview=True
        )
    else:
        if Var.UPDATES_CHANNEL is not None:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "banned":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="⛔️حساب کاربری شما به دلیل تخلف مسدود شده است⛔️",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="📛 برای حمایت از ما و همچنان ربات ابتدا در کانال ما عضو شوید.\n\n✅ پس از عضویت وارد ربات شده و دستور /start را ارسال کنید.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("💠عضویت در کانال💠", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="*",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))

        file_size = None
        if get_msg.video:
            file_size = f"{humanbytes(get_msg.video.file_size)}"
        elif get_msg.document:
            file_size = f"{humanbytes(get_msg.document.file_size)}"
        elif get_msg.audio:
            file_size = f"{humanbytes(get_msg.audio.file_size)}"

        file_name = None
        if get_msg.video:
            file_name = f"{get_msg.video.file_name}"
        elif get_msg.document:
            file_name = f"{get_msg.document.file_name}"
        elif get_msg.audio:
            file_name = f"{get_msg.audio.file_name}"

        stream_link = "https://{}/{}".format(Var.FQDN, get_msg.message_id) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.message_id)

        msg_text = "♻️فایل شما با موفقیت به لینک تبدیل شد\n\n💢نام فایل: {}\n {}\n\n⚠️لینک دانلود نیم بها میباشد، قبل از دانلود VPN خود را خاموش کنید!"
        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬇️لینک دانلود⬇️", url=stream_link)]])
        )


@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"🔆اطلاعیه\n\n🔰کاربر [{message.from_user.first_name}](tg://user?id={message.from_user.id}) وارد ربات شد."
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "banned":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="⛔️حساب کاربری شما به دلیل تخلف مسدود شده است⛔️",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                    text="📛 برای حمایت از ما و همچنان ربات ابتدا در کانال ما عضو شوید.\n\n✅ پس از عضویت وارد ربات شده و دستور /start را ارسال کنید.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("💠عضویت در کانال💠", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]
                        ]
                    ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="*",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text="❗️راهنمای ربات\n\n⇇فایل مورد نظر خود ارسال یا فوروارد کنید\n\n⇇قبل از دانلود VPN را خاموش کنید\n\n⇇لینک های ربات نیم بها میباشد\n\n⇇انقضای فایل ها 30 روز است (در صورت حمایت دائمی میشود)\n\n🆔 @King_Network7", 
  parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔄شروع مجدد🔄", url="https://t.me/King7UpBot?start")]
            ]
        )
    )

@StreamBot.on_message(filters.command('about') & filters.private & ~filters.edited)
async def about_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"🔆اطلاعیه\n\n🔰کاربر [{message.from_user.first_name}](tg://user?id={message.from_user.id}) وارد ربات شد."
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "banned":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="⛔️حساب کاربری شما به دلیل تخلف مسدود شده است⛔️",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                    text="📛 برای حمایت از ما و همچنان ربات ابتدا در کانال ما عضو شوید.\n\n✅ پس از عضویت وارد ربات شده و دستور /start را ارسال کنید.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("💠عضویت در کانال💠", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]
                        ]
                    ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="*",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text="""
        👤درباره ما

↯طراحی: KingNetwork
 (https://t.me/King_network7)↯سرور: Exclusive
↯ورژن: 1.0.2
↯لینک: نیم بها
↯حمایت: دونیت

 (https://www.payping.ir/d/WiZG)🆔 @King_Network7
        """,
  parse_mode="html",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔄شروع مجدد🔄", url="https://t.me/King7UpBot?start")]
            ]
        )
    )
