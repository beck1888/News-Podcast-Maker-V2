import os
import dotenv

dotenv.load_dotenv()

def get_environmental_variable(key: str) -> str:
    return os.getenv(key)
