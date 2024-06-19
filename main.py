from fastapi import FastAPI

import api.routers.data_collector

app = FastAPI()


app.include_router(api.routers.data_collector.data_collection_router)
