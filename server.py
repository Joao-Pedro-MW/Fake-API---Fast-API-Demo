from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from faker import Faker
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt
import os

from autenticador import SECRET_KEY, ALGORITHM

app = FastAPI()
faker = Faker()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

def valida_usuario(token: str = Depends(oauth2_scheme)):
    try:
        # decodificando o token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return username
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")


@app.get("/nome")
async def get_nomes(current_user: TokenData = Depends(valida_usuario)):
    return JSONResponse(content={'nome': faker.unique.first_name()})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=80)