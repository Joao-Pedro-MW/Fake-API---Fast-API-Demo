from passlib.context import CryptContext


usuarios = {
    "foo": {
        "hashed_password": "$2b$12$KIXtUO1Yx92TF/FelP/FSu8fHdzv9VkZzKcfpUS4DlB2vZ4QW.2vG",
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verifica_hash(token: str):
    for user in usuarios.values():
        if pwd_context.verify(token, user["hashed_password"]):
            return True
        else:
            return False
