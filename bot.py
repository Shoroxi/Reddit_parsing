import asyncio
import datetime
import json
import re
import time

from snippets.disc import Discord
from snippets.reddit import Reddit
from snippets.telegram_bot import Telegram
from snippets.vk import Vk


def auth():
    """
    Authentication in reddit app and vk app
    """
    with open('config.txt', 'r+') as f:
        info = eval(f.read())

    vk = Vk()
    tg = Telegram()
    ds = Discord()
    r = Reddit(
        client_id=info['reddit']['client_id'],
        client_secret=info['reddit']['client_secret'],
        user_agent=info['reddit']['user_agent']
    )

    return vk, tg, ds, r

def content_filter(text):
    """
    The simple filter of words
    Change the values in filter.txt to configurate it.
    """
    filter_result = {
        'length': True,
        'count': True,
        'black_list': True
    }

    with open('filter.txt', 'r') as f:
        info = eval(f.read())

    if len(text) < info['min_word_length'] or len(text) > info['max_word_length']:
        filter_result['length'] = False

    if len(text.split(' ')) < info['min_count_of_words'] or len(text.split(' ')) > info['max_count_of_words']:
        filter_result['count'] = False

    for word in info['black_list']:
        if word in text:
            filter_result['black_list'] = False
        break

    return filter_result

def linearSearch(list, value):
    for i in range(len(list)):
        if list[i]["name"] == value:
            return i

async def create_new_posts(vk, tg, ds, r, settings):
    ds_counter = 0
    vk_counter = 0
    tg_counter = 0
    all_counter = 0
    while True:
        new_posts = r.get_new_posts_from_array(**settings['reddit'])
        print(f"\nПоиск в {settings['reddit']['name']}")
        for post in reversed(new_posts):
            if post['url'] is not None:
                allowed_extension = ['jpg', 'jpeg', 'png', 'gif', 'gifv']
                file_extension = re.search("([^.]*)$", post["url"]).group(1).lower()
                if file_extension in allowed_extension:
                    # cons_txt += "Image"
                    pass
                else:
                    continue

            with open('time_post.json', 'r+') as f:
                date = json.load(f)

                flairs = ["----"] # blacklist

                i = linearSearch(date["subreddit"], str(settings['reddit']['name']))
                if i is not None and post["created_at"] > (date["subreddit"][i]["time"]) and post["spoiler"] is False and post["link_flair_text"] not in flairs and post["ups"] > 50:
                    value = datetime.datetime.fromtimestamp(post["created_at"])
                    print(f"URL:{post['url']}, ДАТА: {value.strftime('%H:%M')}")
                    print(f"Тэг: {post['link_flair_text']}")
                    print(f"Ссылка: https://www.reddit.com{post['permalink']}")

                    # TELEGRAM
                    try:
                        if type(date['subreddit'][i]['tg']) is int:
                            tg.start(post['url'], f"{date['subreddit'][i]['tg']}")
                            tg_counter += 1
                    except Exception as e:
                        print(e)

                    # DISCORD
                    list_subs = ["----"] # not embed
                    vk_list = ["----"] # blacklist

                    if settings['reddit']['name'] in list_subs:
                        ds.send(post['url'], post['sub_name'], settings['webhook_url'])
                        ds_counter += 1
                    else:
                        ds.embed(post['url'], post['sub_name'], settings['webhook_url'])
                        ds_counter += 1

                     # VK
                     if settings['reddit']['name'] not in vk_list:
                         try:
                             vk.post(image_url=post['url'], **settings)
                             vk_counter += 1
                         except Exception as e:
                             print(e)
                    
                    all_counter += 1

                    # JSON
                    time_data = {
                        "name": settings['reddit']['name'],
                        "time": post["created_at"],
                        "tg": date['subreddit'][i]['tg']
                    }
                    stats_data = {
                        "Discord Posts": (date["bot"]["Discord Posts"] + ds_counter),
                        "VK Posts": (date["bot"]["VK Posts"] + vk_counter),
                        "TG Posts": (date["bot"]["TG Posts"] + tg_counter),
                        "All Posts": (date["bot"]["All Posts"] + all_counter)
                    }
                    write_json(time_data, i, 'time_post.json')
                    upd_stats_json(stats_data, 'time_post.json')
                else:
                    pass

                if i == ----: # num of subreddits
                    bot_stats = "https://discord.com/api/webhooks/1001414242718720131/QOAOd4H7PocNQkhpIDw_S8rG5EZfUXvQiq3b4LTxgmIQAnNUR3CTtvvZ70MqwJ8KFIO9"
                    ds.edit(date["bot"]["Discord Posts"], date["bot"]["VK Posts"], date["bot"]["TG Posts"], date["bot"]["All Posts"], bot_stats)
                    stats_data = {
                        "Discord Posts": 0,
                        "VK Posts": 0,
                        "TG Posts": 0,
                        "All Posts": (date["bot"]["All Posts"] + all_counter)
                    }
                    upd_stats_json(stats_data, 'time_post.json')

        await asyncio.sleep(settings['delay'])
        print("Отоспались...")

def write_json(data, i, filename):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["subreddit"][i].update(data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

def upd_stats_json(data, filename):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["bot"].update(data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

# def upd_stats(ds):
#     Stat_bot = "https://discord.com/api/webhooks/----"
#     ds.edit(i, Stat_bot)

def main():
    vk, tg, ds, r = auth()

    # upd_stats(ds)

    with open('search_settings.txt', 'r') as f:
        settings = []
        for stroke in f.read().split('\n'):
            setting = eval(stroke)
            try:
                setting['vk']['publish_date'] = time.time() + setting['delay'] + setting['vk']['publish_delay']
                del setting['vk']['publish_delay']
            except:
                pass

            settings.append(setting)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(*[create_new_posts(vk, tg, ds, r, setting) for setting in settings])
    )
    loop.close()


if __name__ == '__main__':

    main()
