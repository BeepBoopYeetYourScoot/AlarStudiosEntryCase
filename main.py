from fastapi import FastAPI

import api.routers.data

app = FastAPI()


app.include_router(api.routers.data.router)
