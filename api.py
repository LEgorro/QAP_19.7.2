import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    def get_api_key(self, email: str, password: str):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON с уникальным ключём
        пользователя, найденного по указанным e-mail и паролем"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON со списком
        всех питомцев, или со списком 'Мои питомцы', если указан фильтр 'my_pets'"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_information_about_new_pet_without_photo(self, auth_key, name: str, animal_type: str, age: str):
        """Метод делает запрос к API сервера о добавлении питомца без фото и возвращает статус запроса и результат
        в формате JSON с данными нового питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_information_about_new_pet(self, auth_key, name: str, animal_type: str, age: str, pet_photo: str):
        """Метод делает запрос к API сервера о добавлении питомца с фото и возвращает статус запроса и результат
        в формате JSON с данными нового питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key, pet_id: str, pet_photo: str):
        """Метод делает запрос к API сервера о добавлении фото питомца по указанному ID и возвращает статус запроса
        и результат в формате JSON с данными питомца"""

        data = MultipartEncoder(
            fields={
                'pet_id': pet_id,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + f'/api/pets/set_photo/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_information_about_pet(self, auth_key, pet_id: str, name: str = '', animal_type: str = '', age: str = ''):
        """Метод делает запрос к API сервера об изменении информации питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с данными питомца"""

        data = MultipartEncoder(
            fields={
                'pet_id': pet_id,
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.put(self.base_url + f'/api/pets/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet_from_database(self, auth_key, pet_id: str):
        """Метод делает запрос к API сервера об удалении питомца по указанному ID и возвращает статус запроса"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result