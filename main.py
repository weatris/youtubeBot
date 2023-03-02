import os

import telebot

from app.worker import add_music_to_video, get_video, get_song, handle_delete_all


bot = telebot.TeleBot('5888000229:AAFj6xqaWLk7l8Z3Qmjoq2OsuwDavo-KrOo')

import pathlib

folder_path = str(pathlib.Path(__file__).parent.resolve())
chat_id = 0

def check_progress(mes):
    print(mes)
    bot.send_message(chat_id, mes)

def create_video(video_filter, music_filter, amount):
    check_progress('Downloading videos')
    get_video(video_filter, int(amount))

    check_progress('Downloading music')
    get_song(music_filter, int(amount)*2)

    check_progress('Adding music ')
    add_music_to_video()

mapper = {
    'video': create_video
}


@bot.message_handler(content_types=['text'])
def get_text_messages(mes):
    try:
        cmd, a, b, c = mes.text.split('\n')
        global chat_id
        chat_id = mes.chat.id
        check_progress('Started working')
        mapper[cmd](a, b, c)

        for filename in os.listdir(folder_path + '\\app\\results'):
            try:
                file_path = os.path.join(folder_path + '\\app\\results\\', filename)
                bot.send_video(mes.chat.id, video=open(file_path, 'rb'), supports_streaming=True)
            except:
                check_progress( f'cant send file : {filename}')
                continue

    except Exception as e:
        print(e)
        check_progress( 'Not this time')
    handle_delete_all()


print('bot started')
bot.polling(none_stop=True)
