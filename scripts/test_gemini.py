import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not api_key:
    raise SystemExit("ERROR: GEMINI_API_KEY belum ditemukan di .env")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model=model,
        contents="Jelaskan secara singkat apa itu Agentic AI dalam bahasa Indonesia."
    )

    print("\n===== GEMINI RESPONSE =====")
    print(response.text)

finally:
    client.close()
