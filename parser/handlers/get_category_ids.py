import requests as requests

from parser import engine
from parser.utils.database.models import main_categories


async def get_category():
    with requests.get(f'https://www.avito.ru/web/1/category/tree') as response:
        result = response.json()
    for category in result['items']:
        if 'parentId' in category:
            entry = main_categories.insert().values(
                category_id=category['id'],
                category_absolute_id=category['categoryId'],
                name=category['name'],
                param_201=category['microcategoryId'],
                parent_id=category['parentId']
            )
        else:
            entry = main_categories.insert().values(
                category_id=category['id'],
                category_absolute_id=category['categoryId'],
                name=category['name'],
                param_201=category['microcategoryId'],
            )
        with engine.connect() as conn:
            conn.execute(entry)
            conn.commit()
        print(entry)
