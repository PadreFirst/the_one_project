import os
import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai.types import HarmCategory, HarmBlockThreshold

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing in .env")

genai.configure(api_key=GOOGLE_API_KEY)

# Disable built-in filters to allow custom prompt logic
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    safety_settings=safety_settings
)

async def check_image(image_path):
    max_retries = 2
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            print(f"DEBUG: Uploading {image_path} to Gemini... (Attempt {retry_count + 1}/{max_retries})")
            
            sample_file = genai.upload_file(path=image_path, display_name="User Photo")
            
            # PROMPT IN ENGLISH
            prompt = (
                "You are a strict content moderator. "
                "Analyze the image and any text inside it."
                "\n\n"
                "STRICTLY FORBIDDEN CONTENT (Return 'FAIL'):\n"
                "1. POLITICS & LEADERS: NO images/mentions of Putin, Zelensky, Biden, Trump, etc. NO political symbols.\n"
                "2. WAR & MILITARY: NO Russia-Ukraine conflict, Z/V symbols, weapons, guns, tanks, soldiers. NO dead bodies.\n"
                "3. HATE SPEECH & SLURS: NO racism, no n-word, no ethnic slurs.\n"
                "4. ADULT CONTENT: NO nudity, pornography, sexual organs.\n"
                "\n"
                "ALLOWED CONTENT:\n"
                "Selfies, ads, memes, landscapes, art.\n"
                "\n"
                "RESPONSE FORMAT:\n"
                "If ALLOWED, return exactly: 'OK'.\n"
                "If FORBIDDEN, return exactly: 'FAIL: <short reason in English>'. Example: 'FAIL: Politics forbidden'."
            )
    
            response = model.generate_content([sample_file, prompt])
            text = response.text.strip()
            print(f"DEBUG: Gemini Response: {text}")
    
            if text.startswith("OK"):
                return True, "OK"
            elif text.startswith("FAIL"):
                reason = text.replace("FAIL:", "").strip()
                return False, reason
            else:
                return False, "AI returned unknown response. Try another photo."
    
        except Exception as e:
            retry_count += 1
            print(f"ERROR in ai_check (attempt {retry_count}): {e}")
            
            if retry_count >= max_retries:
                return False, f"Service temporarily unavailable. Please try again later."
            
            # Небольшая задержка перед повтором
            import asyncio
            await asyncio.sleep(2)