import requests

base_url = 'http://localhost:8001'
food_info_url = f'{base_url}/food_info'
search_food_url = f'{base_url}/search_food'


def test_search_food():
    response = requests.get(f"{search_food_url}?query=salad")
    assert response.status_code == 200
    assert 'products' in response.json()
