from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()
usuarios = {
    # senha = teste
    "foo": {"hashed_password": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmb28iLCJleHAiOjE3MzAzMDQ4NDh9.TB1QRbJBJLXUnB2HcUX04Hcm1UnKt5aclqavDAELq-o",}
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
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def valida_usuario(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # nessa função decodificamos o token criado e verificamos se o usuário realmente existe em nosso 'banco de dados'
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # usa sub, devido ao modelo do token jwt
        username: str = payload.get("sub")
        if username is None or username not in usuarios:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return usuarios[username]
