from discord import Webhook
import requests
from dhooks import Webhook, Embed
import random
import aiohttp

class Discord:

    @staticmethod
    def embed(url, sub, webhook_url):
        hook = Webhook(url=webhook_url, username=sub)
        em = Embed(color=0x5CDBF0, timestamp='now')

        chance = random.random()
        if chance > 0.8:
            em.set_title('----',
                         url="----")

        em.set_image(url)
        # em.set_footer(text=sub)
        hook.send(embed=em)
        print("Запостил в DISCORD")

    @staticmethod
    def send(url, sub, webhook_url):
        hook = Webhook(url=webhook_url, username=sub)
        hook.send(content=url)
        print("Запостил в DISCORD")

    @staticmethod
    def message(txt, webhook_url):
        hook = Webhook(url=webhook_url, username="----")
        hook.send(content=txt)
        print("ПОГНАЛ")

    @staticmethod
    def edit(ds, vk, tg, all1, webhook_url):

        data = {
            "content": f"Постов DS:{ds}\nBK:{vk}\nTG:{tg}\nAll:{all1}"
        }
        message = "/messages/0000"
        requests.patch(webhook_url+message, data)

