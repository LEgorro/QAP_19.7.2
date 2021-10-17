from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_with_invalid_email(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "This user wasn't found in database" in result


def test_get_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "This user wasn't found in database" in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert 'pets' in result.keys()


def test_get_my_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert 'pets' in result.keys()


def test_get_all_pets_with_invalid_key(filter=''):
    auth_key = {'key': 'invalid_key'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert "Please provide 'auth_key' Header" in result


def test_add_new_pet_without_photo_with_valid_data():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name = 'Мак'
    animal_type = 'Маламут'
    age = '2'
    status, result = pf.add_information_about_new_pet_without_photo(auth_key,
                                                                    name=name,
                                                                    animal_type=animal_type,
                                                                    age=age)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_add_new_pet_without_photo_with_invalid_age():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name = 'Мак'
    animal_type = 'Маламут'
    age = '-2'
    status, result = pf.add_information_about_new_pet_without_photo(auth_key,
                                                                    name=name,
                                                                    animal_type=animal_type,
                                                                    age=age)

    assert status == 400
    assert "Parameter 'age' cannot be negative." in result


def test_add_or_change_photo_of_first_pet_in_list_of_my_pets_with_valid_data():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    list_of_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')[1]
    if len(list_of_my_pets["pets"]) > 0:
        id_of_first_pet = list_of_my_pets["pets"][0]["id"]
        status, result = pf.add_photo_of_pet(auth_key,
                                             pet_id=id_of_first_pet,
                                             pet_photo='images\Маламут.jpg')

        assert status == 200
        assert result['id'] == id_of_first_pet
        assert result['pet_photo'] != ''
    else:
        raise Exception('У вас нет добавленных питомцев')


def test_add_or_change_photo_of_first_pet_in_list_of_my_pets_with_invalid_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    list_of_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')[1]
    if len(list_of_my_pets["pets"]) > 0:
        status, result = pf.add_photo_of_pet(auth_key,
                                             pet_id='invalid_pet_id',
                                             pet_photo='images\Борзая.jpg')

        assert status == 400
        assert "Pet with this id wasn't found!" in result
    else:
        raise Exception('У вас нет добавленных питомцев')


def test_add_new_pet_with_photo_with_valid_data():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key,
                                                      name='Буян',
                                                      animal_type='Борзая',
                                                      age='2',
                                                      pet_photo='images\Борзая.jpg')

    assert status == 200
    assert result['name'] == 'Буян'
    assert result['animal_type'] == 'Борзая'
    assert result['age'] == '2'
    assert result['pet_photo'] != ''


def test_add_new_pet_with_photo_with_unsuitable_type_of_photo_file():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key,
                                                      name='Буян',
                                                      animal_type='Борзая',
                                                      age='2',
                                                      pet_photo='images\wrong_format.jpf')

    assert status == 400
    assert "Invalid image format: JPG, PNG, BMP only" in result


def test_update_information_about_first_pet_in_list_of_my_pets_with_valid_data():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    list_of_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')[1]

    if len(list_of_my_pets["pets"]) > 0:
        id_of_first_pet = list_of_my_pets["pets"][0]["id"]
        status, result = pf.update_information_about_pet(auth_key,
                                                         pet_id=id_of_first_pet,
                                                         name='Нико',
                                                         animal_type='Легавая',
                                                         age='3')

        assert status == 200
        assert result['id'] == id_of_first_pet
        assert result['name'] == 'Нико'
        assert result['animal_type'] == 'Легавая'
        assert result['age'] == '3'
    else:
        raise Exception('У вас нет добавленных питомцев')


def test_update_information_about_first_pet_in_list_of_my_pets_with_invalid_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    list_of_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')[1]

    if len(list_of_my_pets["pets"]) > 0:
        status, result = pf.update_information_about_pet(auth_key,
                                                         pet_id='invalid_pet_id',
                                                         name='Нико',
                                                         animal_type='Легавая',
                                                         age='3')

        assert status == 400
        assert "Pet with this id wasn't found!" in result
    else:
        raise Exception('У вас нет добавленных питомцев')


def test_delete_first_pet_in_list_of_me_pets_from_database():
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    list_of_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')[1]

    if len(list_of_my_pets["pets"]) > 0:
        id_of_first_pet = list_of_my_pets["pets"][0]["id"]
        status, result = pf.delete_pet_from_database(auth_key,
                                                     pet_id=id_of_first_pet)

        assert status == 200
        assert result == ''
        my_pets_list = pf.get_list_of_pets(auth_key, filter="my_pets")[1]["pets"]
        for pet in range(len(my_pets_list)):
            assert id_of_first_pet not in my_pets_list[pet].values()
    else:
        raise Exception('У вас нет добавленных питомцев')
