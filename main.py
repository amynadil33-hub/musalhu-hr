from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI
from googletrans import Translator

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

API_KEY = "musalhuX-super-secret-key"

app = FastAPI()
translator = Translator()

class HRRequest(BaseModel):
    message: str
    lang: str = "en"

@app.post("/chat/hr")
async def chat_hr(req: HRRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    text = req.message

    if req.lang == "dv":
        text = translator.translate(text, src="dv", dest="en").text

    # ✅ New SDK call
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Musalhu HR Assistant for Maldivian SMEs."},
            {"role": "user", "content": text}
        ]
    )

    output = completion.choices[0].message.content

    if req.lang == "dv":
        output = translator.translate(output, src="en", dest="dv").text

    return {"output": output}
