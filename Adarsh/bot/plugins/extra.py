from Adarsh.bot import StreamBot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
import time
import shutil, psutil
from utils_bot import *
from Adarsh import StartTime

        
    
@StreamBot.on_message(filters.command('stats') & filters.private & ~filters.edited)
async def stats(bot, update):
  currentTime = readable_time((time.time() - StartTime))
  total, used, free = shutil.disk_usage('.')
  total = get_readable_file_size(total)
  used = get_readable_file_size(used)
  free = get_readable_file_size(free)
  sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
  recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
  cpuUsage = psutil.cpu_percent(interval=0.5)
  memory = psutil.virtual_memory().percent
  disk = psutil.disk_usage('/').percent
  botstats = f'⚛️آپ تایم : {currentTime}\n' \
            f'📊فضا سرور: {total}\n' \
            f'📈فضا استفاده شده: {used}\n' \
            f'📉فضا باقی مانده: {free}\n\n' \
            f'⏱سرعت آپلود : {sent}\n' \
            f'⏱سرعت دانلود : {recv}\n\n' \
            f'<b>CPU:</b> {cpuUsage}% ' \
            f'<b>RAM:</b> {memory}% ' \
            f'<b>Disk:</b> {disk}%\n\n 🆔 @King_Network7'
  await update.reply_text(botstats)
