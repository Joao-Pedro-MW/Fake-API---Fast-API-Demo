from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from faker import Faker

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from autenticador import autentica, cria_token

app = FastAPI()
faker = Faker()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

@app.get("/nome")
async def get_nomes(token: str = Depends(oauth2_scheme)):
    return JSONResponse(content=['Nome', faker.unique.first_name()])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=80)
