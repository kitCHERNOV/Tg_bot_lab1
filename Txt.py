import MukeshAPI
import telebot 
from Main import *
import os
import yt_dlp


#===========================================================================Image
def gen_img(msg):
        
    try:
        img = MukeshAPI.api.ai_image(msg.text)
        bot.send_photo(msg.chat.id, img, msg.text)
        return
    except:
        bot.send_message(msg.chat.id,"Не удалось отправить изображение")
        bot.register_next_step_handler(msg, gen_img)
        
def send_img(msg):
    try:
        bot.send_photo(msg.chat.id, msg.text)
        return
    except Exception as ex:
        bot.send_message(msg.chat.id,f"Не удалось отправить изображение: {ex}")
        bot.register_next_step_handler(msg, send_img)
        
@bot.callback_query_handler(func=lambda call: call.data == IMG_BTNS[1][1])
def link(call:telebot.types.CallbackQuery):
    msg = call.message
    bot.edit_message_text("Отправьте ссылку", msg.chat.id,msg.id)
    bot.register_next_step_handler(msg, send_img)

@bot.callback_query_handler(func=lambda call: call.data == IMG_BTNS[0][1])
def link(call:telebot.types.CallbackQuery):
    msg = call.message
    bot.edit_message_text("Отправьте запрос", msg.chat.id,msg.id)
    bot.register_next_step_handler(msg, gen_img)
@bot.callback_query_handler(func=lambda call: call.data == START_BTNS[0][1])
def image_btn(call:telebot.types.CallbackQuery):
    msg = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = [telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data) for text, callback_data in IMG_BTNS]
    keyboard.add(*buttons)
    bot.edit_message_text("Работа с изображением", msg.chat.id,msg.id,reply_markup=keyboard)

#============================================================================audio
def download_audio(anime_title):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': ('downloads/'+str(anime_title)+'.mp3'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch:{anime_title} opening", download=True)
            if search_results['entries']:
                video_url = search_results['entries'][0]['url']
                ydl.download([video_url])
                audio_file = f"downloads/{anime_title}.mp3"
                if os.path.exists(audio_file):
                    return audio_file
                else:
                    return None
            else:
                return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def Inputanime(msg:telebot.types.Message):
    audio_file = download_audio(msg.text)
    if audio_file and os.path.exists(audio_file):
        with open(audio_file, 'rb') as audio:
            bot.send_audio(msg.chat.id,audio)
        os.remove(audio_file)  # Удаляем файл после отправки
    else:
        bot.reply_to(msg.text, "Не удалось найти опенинг для указанного аниме.")
    



@bot.callback_query_handler(func=lambda call: call.data == AUDIO_BTNS[0][1])
def tts_audio(call: telebot.types.CallbackQuery):
    call = call.message
    bot.edit_message_text("Отправьте название аниме для получения опенинга:", call.chat.id, call.id)
    bot.register_next_step_handler(call,Inputanime)

    

@bot.callback_query_handler(func=lambda call: call.data == START_BTNS[1][1])
def audio_btn(call: telebot.types.CallbackQuery):
    msg = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = [telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data) for text, callback_data in AUDIO_BTNS]
    keyboard.add(*buttons)
    bot.edit_message_text("Работа с аудио", msg.chat.id, msg.id, reply_markup=keyboard)
#=========================================================================Repositori
@bot.callback_query_handler(func=lambda call: call.data == START_BTNS[2][1])
def scource_btn(call:telebot.types.CallbackQuery):
    msg = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text=f"Репозиторий", url=REP_URL)
    keyboard.add(button)
    bot.edit_message_text(REP_URL, msg.chat.id,msg.id,reply_markup=keyboard)

#====================================================================Ending
@bot.message_handler(commands=["start"])
def start(msg:telebot.types.Message):
    chat_id = msg.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = [telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data) for text, callback_data in START_BTNS]
    keyboard.add(*buttons)
    return bot.send_message(chat_id,
                            START_MSG,
                            reply_markup= keyboard)

bot.polling()

