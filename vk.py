import re
import time
import json

import requests
import vk_api


class Vk:
    def __init__(self):
        self.v = '6.0.0'
        self.auth()

    def auth(self):
        with open('config.txt', 'r') as f:
            info = eval(f.read())
            self.group_id = info['vk']['group_id']
            self.album_id = 0000
            access_token = info['vk']['access_token']

        session = vk_api.VkApi(token=access_token)
        self.api = session.get_api()

    def save_to_album(self, album_id):
        self.api.photos.getUploadServer(album_id=album_id, group_id=self.group_id, v=self.v)

    def post(self, **kwargs):
        if 'image_url' in kwargs.keys():
            destination = self.api.photos.getWallUploadServer(group_id=self.group_id, v=self.v)
            album = self.api.photos.getUploadServer(album_id=self.album_id, group_id=self.group_id, v=self.v)
            file_extension = re.search("([^.]*)$", kwargs['image_url']).group(1).lower()

            if file_extension in ['jpg', 'jpeg', 'png']:
                image = requests.get(kwargs['image_url'], stream=True)

                data = ("image.jpg", image.raw, image.headers['Content-Type'])
                meta = requests.post(destination['upload_url'], files={'photo': data}).json()
                photo = self.api.photos.saveWallPhoto(group_id=self.group_id, **meta, v=self.v)[0]
                # meta2 = requests.post(url=album['upload_url'], files={'photo': data}).json()
                # self.api.photos.save(album_id=self.album_id, group_id=self.group_id, **meta2, v=self.v)


                try:
                    kwargs['attachments'] += f",photo{photo['owner_id']}_{photo['id']}"
                except:
                    kwargs['attachments'] = f"photo{photo['owner_id']}_{photo['id']}"

                del kwargs['image_url']
                if photo is not None:
                    self.api.wall.post(
                        owner_id=-self.group_id,
                        v=self.v,
                        message=f"#nsfw #porn #{kwargs['reddit']['name']}@stipbar",
                        attachments=f"photo{photo['owner_id']}_{photo['id']}"
                        # **kwargs
                        )

                    print(f"Запостил в ВК")
                    time.sleep(3)

            else:
                print("вк не поддержит формат")
                pass

            # else:
            #     self.api.wall.post(
            #         owner_id=-self.group_id,
            #         v=self.v,
            #         attachments=f"video{video['owner_id']}_{video['id']}"
            #         # **kwargs
            #         )
