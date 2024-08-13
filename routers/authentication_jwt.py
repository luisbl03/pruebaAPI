from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITMO = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "a08424bb13b0a4057f68131702f9e5ba2c893c72405419f93c1fc07a2d24787f"


oauth2 = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "darthvader": {
        "username": "darthvader",
        "full_name": "Anakin Skywalker",
        "email": "starwarsmola@gmail.com",
        "disabled": False,
        "password": "$2a$12$Zcimwo.hwh3giHpqS.Dd4uOXievlM5JoJ5e5OyQboBN7YWQLwPSR2" 
    },
    "yoda": {
        "username": "yoda",
        "full_name": "Yoda",
        "email": "yoda@gmail.com",
        "disabled": True,
        "password": "$2a$12$/PqgUfP3xr9C4Ggjh/GvH.SA3UlUzqwbwNVcoCgSex6Q6DAKBEbRS"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token:str = Depends(oauth2)):
    execption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                              detail="Credenciales invalidas", 
                              headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITMO]).get("sub")
        if username is None:
            raise execption
    except JWTError:
        raise execption

    user = search_user(username)
    if not user:
        raise execption
    
    return user
    
    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario deshabilitado")
    return user

@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Usuario no es correcto")

    user = search_user_db(form.username)


    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña no es correcta")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_DURATION)

    expire = datetime.utcnow() + access_token_expires

    acces_token = {"sub":user.username, "exp":expire}
    
    return {"access_token": jwt.encode(acces_token, SECRET,algorithm=ALGORITMO), "token_type":"bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user