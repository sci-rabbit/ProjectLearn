# import asyncio
import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI

from routes.routes import user_router

# from db.session import setup_db

app = FastAPI()
main_api_route = APIRouter()
main_api_route.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_route)

#
# async def main():
#     await setup_db()


if __name__ == "__main__":
    # asyncio.run(main())
    uvicorn.run("main:app", reload=True)
