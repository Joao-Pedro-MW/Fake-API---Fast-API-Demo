from fastapi import FastAPI
from fastapi.responses import JSONResponse
from faker import Faker

app = FastAPI()
faker = Faker()

@app.get("/nome")
async def get_nomes():
    return JSONResponse(content={'nome': faker.unique.first_name()})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=80)
