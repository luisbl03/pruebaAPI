from fastapi import FastAPI, HTTPException
from routers import products, users, authentication_jwt, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(authentication_jwt.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message":"Hello World"}

