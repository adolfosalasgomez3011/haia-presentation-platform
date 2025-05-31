from dotenv import load_dotenv
import os

load_dotenv()
print("RAPIDAPI_KEY =", os.getenv("RAPIDAPI_KEY"))
