import requests

base_url = 'http://localhost:8000'
add_dish_url = f'{base_url}/add_dish'
get_dishes_url = f'{base_url}/dishes'
get_dish_by_id_url = f'{base_url}/get_dish_by_id'
delete_dish_url = f'{base_url}/delete_dish'

new_dish = {
    "id": 99,
    "name": "Caesar Salad",
    "calories": 150,
    "price": 7.99
}


def test_1_add_dish():
    response = requests.post(add_dish_url, json=new_dish)
    assert response.status_code == 200
    assert response.json()['name'] == new_dish['name']


def test_2_get_dishes():
    response = requests.get(get_dishes_url)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_3_get_dish_by_id():
    response = requests.get(f"{get_dish_by_id_url}/99")
    assert response.status_code == 200
    assert response.json()['id'] == 99


def test_4_delete_dish():
    delete_response = requests.delete(f"{delete_dish_url}/99")
    assert delete_response.status_code == 200

    response = requests.get(f"{get_dish_by_id_url}/99")
    assert response.status_code == 404
