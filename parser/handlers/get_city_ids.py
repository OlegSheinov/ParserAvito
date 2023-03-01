import requests
from fastapi import HTTPException


async def get_city(city_name):
    with requests.get(f'https://www.avito.ru/web/1/slocations?limit=1&q={city_name}') as response:
        result = response.json()
    try:
        return {"id": result["result"]["locations"][0]['id'], "name": result["result"]["locations"][0]["names"]['1']}
    except IndexError:
        raise HTTPException(status_code=404, detail="Не найдено ни одного города по запросу. Повторите попытку!")
