from classes import VK, YandexDisk

'''Указать свой токен'''
with open('C:\\Users\\Алина\\Desktop\\tokens\\token_vk2.txt') as file:
    TOKEN = file.read().strip()
with open ('C:\\Users\\Алина\\Desktop\\tokens\\token_ya_disc.txt') as file:
    TOKEN_ya = file.read()


def main(id,photo_count):
    vk = VK(TOKEN, '5.131')
    ya = YandexDisk(token=TOKEN_ya)
    data = vk.get_name_url_max_size(id,photo_count)
    vk.result_json(id, photo_count, data)
    ya.create_folder(id)
    ya.upload_to_disk(id, dict(data), photo_count)


if __name__ == '__main__':
    user_id = int(input('Укажите id профиля для получения фото: '))
    user_photo_count = int(input('Укажите количество фотографий для загрузки: '))
    main(id=user_id, photo_count=user_photo_count)





