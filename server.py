from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from faker import Faker
from pydantic import BaseModel
from autenticador import autentica, cria_token, valida_usuario

app = FastAPI()
faker = Faker()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    username: str
    password: str

@app.post("/token")
async def login(login: Login):
    usuario = autentica(login.username, login.password)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    token = cria_token({"sub": login.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/nome")
async def get_nomes(current_user: dict = Depends(valida_usuario)):
    return JSONResponse(content={'nome': faker.unique.first_name()})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
