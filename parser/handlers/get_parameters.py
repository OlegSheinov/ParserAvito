import re
from urllib.parse import urlencode, unquote

import requests


async def get_main_category():
    with requests.get("https://www.avito.ru/web/1/category/tree") as response:
        result: dict = response.json()
    all_categories = [{"id": obj['categoryId'], "name": obj['name']} for obj in result['items'] if
                      not obj.get('parentId')]
    return all_categories


async def get_subcategory(category_id, parent_category_id=None):
    with requests.get("https://www.avito.ru/web/1/category/tree", timeout=5) as response:
        result: dict = response.json()
    if not parent_category_id:
        main_category = next(filter(lambda obj: obj['categoryId'] == category_id, result['items']), None)
        all_subcategories = [
            {"id": obj['categoryId'], "name": obj['name'], "forParentId": obj['id'],
             "param": list(map(lambda x: unquote(x),
                               re.findall(r"params%5B\d+%5D=\d+", obj.get('deeplink', None)) if obj.get('deeplink',
                                                                                                        None) else ''))}
            for obj in result['items'] if obj.get('parentId', None) == main_category['id']]
    else:
        all_subcategories = [
            {"id": obj['categoryId'], "name": obj['name'], "forParentId": obj['id'],
             "param": list(map(lambda x: unquote(x),
                               re.findall(r"params%5B\d+%5D=\d+", obj.get('deeplink', None)) if obj.get('deeplink',
                                                                                                        None) else ''))}
            for obj in result['items'] if obj.get('parentId', None) == parent_category_id]
    return all_subcategories


async def get_params(data, type_params, all_filters=None):
    match type_params:
        case "main_category":
            return await get_main_category()
        case "subcategory":
            return await get_subcategory(data['categoryId'], data.get('parentId'))
        case "filters":
            url = "https://m.avito.ru/api/6/search/parameters?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"
            params = urlencode([(k, v) for k, v in data.items() if v is not None])
            with requests.get(f"{url}&{params}") as response:
                result = response.json()
            all_select = list(
                filter(lambda obj: obj['id'] != 'sort' and obj['type'] == 'select', result['result']['params']))
            all_multiselect = list(filter(lambda obj: obj['type'] == 'multiselect', result['result']['params']))
            all_groups = list(filter(
                lambda obj: any(item in obj['id'] for item in ["param", "price", "brand"]) and obj['type'] == 'group',
                result['result']['params']))
            print(result)
            return all_select, all_multiselect, all_groups
