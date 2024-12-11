from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import config
import openai

openai.api_key = config.apiToken()

client = openai.OpenAI()

app = FastAPI()

class AGIInquiries(BaseModel):
    input_str: str

def askAggie(input_str):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "assistant":"aggie",
                "content": input_str,
            }
        ],
    )

    return completion.choices[0].message.content

@app.post("/askAggie/")  # This line decorates 'translate' as a POST endpoint
async def inquiryAGI(request: AGIInquiries):
    try:
        # Call your translation function
        answer = askAggie(request.input_str)
        return {"answer": answer}
    except Exception as e:
        # Handle exceptions or errors during translation
        raise HTTPException(status_code=500, detail=str(e))