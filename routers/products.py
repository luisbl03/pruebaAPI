from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products"], 
                   responses={404: {"message":"No encontrado"}})

products_list = ["Product1", "Product2", "Product3"]

@router.get("/")
async def get_products():
    return products_list

@router.get("/{id}")
async def get_product(id:int):
    return products_list[id]