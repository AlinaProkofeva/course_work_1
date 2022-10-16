import json
import requests
from datetime import  datetime
import os
import time
from tqdm import tqdm

class Progress:
    '''создаем прогресс-бар'''
    def progress(self):
        my_list = [1, 2, 3]
        for i in tqdm(my_list):
            time.sleep(1)
progress_bar = Progress()

class VK():
    '''создаем класс для работы с VK'''
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def _get_photos(self, id):
        '''получение фотографий профиля по id'''
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'owner_id': id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'rev': 1,
            # 'photo_sizes': 1,
            'count': 5
        }
        res = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        return res['response']['items']

    def get_name_url_max_size(self, id):
        '''получаем словарь: имя фото и ссылку на него в максимальном размере'''
        result_photo_dict = {}
        for i in self._get_photos(id):
            name_part_1 = str(i['likes']['count']) # показывает лайки
            name_part_2 = datetime.utcfromtimestamp(i['date']).strftime('%Y_%m_%d_%H_%M_%S') # показывает дату загрузки
            filename = name_part_1 + '_' + name_part_2 # имя лайки + дата загрузки
            result_photo_dict[filename] = \
                (sorted(list(zip([el['height'] for el in i['sizes']], [el['width'] for el in i['sizes']],
                                 [el['url'] for el in i['sizes']])))[-1])
        return result_photo_dict

    def result_json(self, id):
        '''запись инфо по фото в json'''
        PATH = os.getcwd()
        FULLPATH = os.path.join(PATH, 'result.json') # адрес файла для записи
        data_raw = self.get_name_url_max_size(id)
        data_list = []
        for i, k in data_raw.items():
            data_dict = {}
            data_dict['file_name'] = f'{i}.jpg'
            data_dict['size'] = f'{k[0]}x{k[1]}'
            data_list.append(data_dict)
        print(f'\nПолучаем фотографии профиля')
        progress_bar.progress()
        print(f'\nПолучаем ссылку для фото необходимых размеров')
        progress_bar.progress()
        print(f'\nЗаписываем файл result')
        progress_bar.progress()

        with open (FULLPATH, 'w') as file_obj:
            json.dump(data_list, file_obj, indent=4)


class YandexDisk:
    '''создаем класс для работы с яндекс диском'''
    def __init__(self, token):
        self.token = token
        self.url = 'https://cloud-api.yandex.net' # базовый url

    def get_headers(self):
        return {
            'Content-Type':'application/json',
            'Authorization':f'OAuth {self.token}'
        }

    def create_folder(self,id):
        '''создание папки на яндекс диске для указанного id в вк'''
        create_folder_url = self.url + '/v1/disk/resources'
        create_folder_params = {
            'path': f'disk:/{id}'
        }
        headers = self.get_headers()
        response = requests.put(create_folder_url, params=create_folder_params, headers=headers)
        if response.status_code == 201:
            print(f'\nсоздаем папку на диске:')
            progress_bar.progress()
            print(f'папка {id} создана')

    def upload_to_disk(self, id, photo_dict):
        '''загрузка фото id в папку на диске'''
        upload_url = self.url + '/v1/disk/resources/upload'
        for key, value in photo_dict.items():
            upload_params = {
                'path': f'disk:/{id}/{key}.jpg',
                'url': f'{value[2]}',
                'overwrite': 'true'
            }
            headers = self.get_headers()
            response = requests.post(upload_url, params=upload_params, headers=headers)
            if response.status_code == 202:
                print(f'\n\nЗагружаем фото {key}:')
                progress_bar.progress()
                print(f'\nфайл {key}.jpg загружен в папку {id}')