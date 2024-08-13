from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"] )

class User(BaseModel):
    id: int
    nombre:str
    apellido:str
    url:str
    edad:int


users_list = [User(id=1,nombre = "Luis", apellido="Benito", url="http://luisbenito.com", edad=30),
         User(id=2,nombre = "Juan", apellido="Perez", url="http://juanperez.com", edad=25),
         User(id=3,nombre = "Maria", apellido="Gomez", url="http://mariagomez.com", edad=35)]


#***OPERACIONES GET***
@router.get("/usersjson")
async def getUsers():
    return [{"nombre":"Luis", "apellido":"Benito"},
            {"nombre":"Juan", "apellido":"Perez"},
            {"nombre":"Maria", "apellido":"Gomez"}]


@router.get("/users")
async def getUsers():
    return users_list

@router.get("/user/{id}")
async def getUser(id:int):
    return buscar_usuario(id)

@router.get("/userquery")
async def getUser(id:int):
    return buscar_usuario(id)
    #al escribir el enlace, se debe escribir una interrogacion, junto con el nombre del parametro a buscar y su valor

def buscar_usuario(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"message":"User not found"}
    
#***OPERACIONES POST***
@router.post("/user/", status_code=201)
async def createUser(user:User):
    if type(buscar_usuario(user.id)) == User: 
        raise HTTPException(status_code=404, detail="Usuario ya existe")
    
    users_list.append(user)
    return user

#***OPERACIONES PUT***
@router.put("/user/")
async def updateUser(user:User):

    found = buscar_usuario(user.id)

    for index, save in enumerate(users_list):
        if save.id == user.id:
            users_list[index] = user
            found = True
            return user
    if not found:
        return {"message":"User not found"}

#***OPERACIONES DELETE***
@router.delete("/user/{id}")
async def deleteUser(id:int):
    found = buscar_usuario(id)
    if type(found) == User:
        users_list.remove(found)
        return {"message":"User deleted"}
    else:
        return {"message":"User not found"}
