import os
import telebot
from telebot import types
from yt_dlp import YoutubeDL

TOKEN = "8797215443:AAFPGG4RZBOhIs2J1oqThW4yPFWaBv2IpH4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🎵 Musiqa yuklash")
    btn2 = types.KeyboardButton("ℹ️ Bot haqida")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Xush kelibsiz! Musiqa nomini yuboring:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "🎵 Musiqa yuklash":
        bot.send_message(message.chat.id, "Musiqa nomi yoki ijrochini yozib yuboring!")
    elif message.text == "ℹ️ Bot haqida":
        bot.send_message(message.chat.id, "Ushbu bot musiqa qidirish va yuklab berish uchun yaratilgan.")
    else:
        msg = bot.send_message(message.chat.id, "🔍 Musiqa qidirilmoqda, kuting...")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'song.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{message.text}", download=True)
                title = info['entries'][0]['title']
            
            with open("song.mp3", 'rb') as audio:
                bot.send_audio(message.chat.id, audio, title=title)
            
            os.remove("song.mp3")
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.send_message(message.chat.id, "❌ Musiqa topilmadi yoki yuklashda xatolik yuz berdi.")

bot.polling(none_stop=True)
