from urllib.parse import urlencode

import requests


async def check_subcategory(result, category_id):
    match category_id:
        case 4:
            pass
        case 1:
            category_group = next(filter(lambda obj: obj['id'] == 'categoryGroup', result['result']['params']), None)
            all_subcategories = next(filter(lambda obj: obj['id'] == 'categoryId', category_group['parameters']), None)
            return all_subcategories['values']


async def get_params(data, type_params, all_filters=None):
    url = "https://m.avito.ru/api/6/search/parameters?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"
    query = [(k, v) for k, v in data.items() if v is not None]
    params = urlencode(query)
    with requests.get(f"{url}&{params}") as response:
        result = response.json()
    match type_params:
        case "main_category":
            category_group = next(filter(lambda obj: obj['id'] == 'categoryGroup', result['result']['params']), None)
            all_categories = next(filter(lambda obj: obj['id'] == 'categoryId', category_group['parameters']), None)
            return all_categories['values']
        case "subcategory":
            return await check_subcategory(result, data['categoryId'])
        case "filters":
            all_select = list(
                filter(lambda obj: obj['id'] != 'sort' and obj['type'] == 'select', result['result']['params']))
            all_multiselect = list(filter(lambda obj: obj['type'] == 'multiselect', result['result']['params']))
            all_groups = list(filter(
                lambda obj: any(item in obj['id'] for item in ["param", "price", "brand"]) and obj['type'] == 'group',
                result['result']['params']))
            return all_select, all_multiselect, all_groups
    print(result)


tet = [
    {"id": 1},
    {"id": 2},
    {"id": 3},
    {"id": 4},
    {"id": 5},
    {"id": 6},
]
