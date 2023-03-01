import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from parser.handlers.get_city_ids import get_city
from parser.handlers.get_parameters import get_params
from parser.utils.database.pydantic_models import DataCity, DataAnnouncementAndParams

app = FastAPI()


@app.get("/get_city_id/")
async def get_city_id(data: DataCity):
    return jsonable_encoder(await get_city(data.name))


@app.get("/get_main_categories/")
async def get_main_categories(data: DataAnnouncementAndParams):
    return jsonable_encoder(await get_params(data.dict(), "main_category"))


@app.get("/get_subcategories/")
async def get_subcategories(data: DataAnnouncementAndParams):
    return jsonable_encoder(await get_params(data.dict(), "subcategory"))


@app.get("/get_filters/")
async def get_parameters(data: DataAnnouncementAndParams):
    return jsonable_encoder(await get_params(data.dict(), "filters", data.filters))


@app.get("/get_announcement/")
async def get_ad(data: DataAnnouncementAndParams):
    print(data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
