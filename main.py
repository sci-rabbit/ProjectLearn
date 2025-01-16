import asyncio

import uvicorn
from fastapi import FastAPI, APIRouter

from db.session import setup_db
from routes.routes import user_router

app = FastAPI()
main_api_route = APIRouter()
main_api_route.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_route)

#
# async def main():
#     await setup_db()


if __name__ == '__main__':
    # asyncio.run(main())
    uvicorn.run("main:app", reload=True)