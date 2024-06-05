import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    persist_directory = os.getenv("PERSIST_DIRECTORY", "persist_dir")
    model = os.getenv("MODEL", "gpt-3.5-turbo")
    temperature = float(os.getenv("TEMPERATURE", 0))
    max_tokens = int(os.getenv("MAX_TOKENS", 1000))
    embed_model = os.getenv("EMBED_MODEL", "text-embedding-3-small")
    pdfs_folder = os.getenv("PDFS_FOLDER", "pdfs")

settings = Settings()
