
import os
from dotenv import load_dotenv

users_db = {
    "foo": {
        "senha": "$2b$12$KIXtUO1Yx92TF/FelP/FSu8fHdzv9VkZzKcfpUS4DlB2vZ4QW.2vG",
    }
}

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))