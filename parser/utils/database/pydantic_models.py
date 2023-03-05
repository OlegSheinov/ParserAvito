from typing import Tuple, Dict

from pydantic import BaseModel


class DataCity(BaseModel):
    name: str


class DataAnnouncementAndParams(BaseModel):
    params: str = None
    categoryId: int = None
    locationId: int = None
    geoCoords: Tuple[float, float] = None
    filters: bool = False
    radius: int = None
    parentId: int = None


# https://m.avito.ru/api/6/search/parameters?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&categoryId=20&locationId=637640


# https://m.avito.ru/api/11/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&params[45]=148&categoryId=20&
# locationId=637640&geoCoords=55.755814,37.617635&localPriority=0&page=2&lastStamp=1677061800&display=list&limit=25&
# pageId=H4sIAAAAAAAA_0q0MrSqLrYyNLRSKskvScyJT8svzUtRss60MjIxNDA0ta4FBAAA___YNQcPIgAAAA&presentationType=serp
