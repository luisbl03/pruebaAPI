def user_scheme(user) -> dict:
    return {
        "id":str(user["_id"]),
        "nombre":user["nombre"],
        "email":user["email"]
    }

def users_scheme(users) -> list:
    return [user_scheme(user) for user in users]