from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import openai
import os
from googletrans import Translator

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🔒 Fixed Musalhu key (no env var confusion)
API_KEY = "musalhuX-super-secret-key"

app = FastAPI()
translator = Translator()

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
        text = translator.translate(text, src="dv", dest="en").text

    # Call OpenAI
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Musalhu HR Assistant for Maldivian SMEs."},
            {"role": "user", "content": text}
        ]
    )

    output = completion.choices[0].message["content"]

    # Translate back if Dhivehi requested
    if req.lang == "dv":
        output = translator.translate(output, src="en", dest="dv").text

    return {"output": output}
