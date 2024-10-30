from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

usuarios = {
    "foo": {
        "hashed_password": "$2b$12$KIXtUO1Yx92TF/FelP/FSu8fHdzv9VkZzKcfpUS4DlB2vZ4QW.2vG",
    }
}

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def valida_senha(input, senha):
    return pwd_context.verify(input, senha)

def get_hash(password):
    return pwd_context.hash(password)

def autentica(usuario: str, senha: str):
    user = usuarios.get(usuario)
    if not user:
        return False
    if not valida_senha(senha, user["hashed_password"]):
        return False
    return user

def cria_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
