import os
import dotenv

dotenv.load_dotenv()

# Model Configuration
# Hybrid Model Configuration
# Heavy: For complex reasoning (Gemini)
HEAVY_MODEL = os.getenv("HEAVY_MODEL", "gemini-1.5-flash")

# Lite: For simple tasks (OpenRouter)
LITE_MODEL = os.getenv("LITE_MODEL", "openai/nex-agi/deepseek-v3.1-nex-n1:free")
