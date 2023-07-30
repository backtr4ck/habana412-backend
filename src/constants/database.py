import os

from dotenv import load_dotenv

load_dotenv()

MONGO_STRING = os.getenv("MONGO_STRING")
DATABASE_NAME = os.getenv("DATABASE_NAME")
