import requests
from pprint import pprint
from classes import VK, YandexDisk


with open('C:\\Users\\Алина\\Desktop\\tokens\\token_vk2.txt') as file:
    TOKEN = file.read().strip()
with open ('C:\\Users\\Алина\\Desktop\\tokens\\token_ya_disc.txt') as file:
    TOKEN_ya = file.read()


def main(id):
    vk = VK(TOKEN, '5.131')
    ya = YandexDisk(token=TOKEN_ya)
    photo_dict = dict(vk.get_name_url_max_size(id))
    vk.result_json(id)
    ya.create_folder(id)
    ya.upload_to_disk(id, photo_dict)


if __name__ == '__main__':
    main(id=1)
