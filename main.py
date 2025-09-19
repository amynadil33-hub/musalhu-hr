from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI

# Try multiple googletrans forks for Translator
try:
    from googletrans import Translator
except ImportError:
    try:
        from googletrans.client import Translator
    except ImportError:
        from google_trans_new import google_translator as Translator

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fixed Musalhu API key
API_KEY = "musalhuX-super-secret-key"

app = FastAPI()

# Initialize translator safely
translator = Translator() if callable(Translator) else Translator

class HRRequest(BaseModel):
    message: str
    lang: str = "en"  # "en" = English, "dv" = Dhivehi

@app.post("/chat/hr")
async def chat_hr(req: HRRequest, x_api_key: str = Header(None)):
    # Security check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    text = req.message

    # Translate Dhivehi → English if needed
    if req.lang == "dv":
        try:
            text = translator.translate(text, src="dv", dest="en").text
        except Exception:
            pass  # fallback if translation fails

    # Call OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Musalhu HR Assistant for Maldivian SMEs."},
            {"role": "user", "content": text}
        ]
    )

    output = completion.choices[0].message.content

    # Translate back to Dhivehi if needed
    if req.lang == "dv":
        try:
            output = translator.translate(output, src="en", dest="dv").text
        except Exception:
            pass

    return {"output": output}
