import os
import dotenv

dotenv.load_dotenv()

# Model Configuration
MODEL = os.getenv("MODEL", "gemini-1.5-flash")
