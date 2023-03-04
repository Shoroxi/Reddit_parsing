import telebot
import re
import time


tg = telebot.TeleBot("----")

class Telegram:

    @staticmethod
    def start(url, tg_group_id):
        file_extension = re.search("([^.]*)$", url).group(1).lower()
        try:
            if file_extension in ['jpg', 'jpeg', 'png']:
                tg.send_photo(tg_group_id,
                              photo=url,
                              caption="",
                              parse_mode='HTML')

            elif file_extension in ['gif', 'gifv']:
                tg.send_animation(tg_group_id,
                                  animation=url,
                                  caption="",
                                  parse_mode='HTML')
            print("Запостил в TELEGRAM")
        except Exception as e:
            print(e)

        # elif file_extension in ["mp4"]:
        #     tg.send_video(tg_group_id,
        #                   video=f'{url}',
        #                   caption="",
        #                   parse_mode='HTML')

        time.sleep(3)

# #============== Запуск🚀
# bot.polling(none_stop=True, interval=0)
