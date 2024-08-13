from fastapi import APIRouter, HTTPException, status
from db.modelos.user import User
from db.client import dbclient
from db.schemas.user import user_scheme, users_scheme
from bson import ObjectId

router = APIRouter(tags=["userdb"],
                   prefix="/userdb",
                   responses={404: {"description": "Not found"}})




#***OPERACIONES GET***

@router.get("/", response_model=list[User])
async def getUsers():
    return users_scheme(dbclient.users.find())

@router.get("/{id}")
async def getUser(id:str):
    return buscar_usuario(campo="_id", key=ObjectId(id))

@router.get("/")
async def getUser(id:str):
   return buscar_usuario(campo="_id", key=ObjectId(id))
    #al escribir el enlace, se debe escribir una interrogacion, junto con el nombre del parametro a buscar y su valor

def buscar_usuario(campo:str, key):
    
    try:
        return User(**user_scheme(dbclient.users.find_one({campo:key})))
    except:
        return {"message":"User not found"}
    
#***OPERACIONES POST***
@router.post("/", status_code=status.HTTP_201_CREATED)
async def createUser(user:User):
    if type(buscar_usuario(campo="email",key=user.email)) == User: 
        raise HTTPException(status_code=404, detail="Usuario ya existe")
    
    user_dict = dict(user)
    del user_dict["id"]

    id = dbclient.users.insert_one(user_dict).inserted_id

    new_user = user_scheme(dbclient.users.find_one({"_id":id})) 
    return User(**new_user)

#***OPERACIONES PUT***
@router.put("/", response_model=User)
async def updateUser(user:User):
    user_dict = dict(user)
    del user_dict["id"]

    try:        
        dbclient.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    except:
        return {"message":"El usuario no se ha podido actualizar"}
    
    return buscar_usuario(campo="_id", key=ObjectId(user.id))

#***OPERACIONES DELETE***
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(id:str):
    found = dbclient.users.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        return {"message":"User not found"}
