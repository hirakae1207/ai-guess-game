from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from google import genai
from dotenv import load_dotenv
import os

from router import router

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI()

@app.get("/")
def read_root():
    return{"message": "Hello, ai-guess-game!"}

@app.get("/test-gemini")
def test_gemini():
    response = client.models.generate_content(
    model= "gemini-3.1-flash-lite",
    contents= "あなたはマジカルバナナに似たゲームに参加しています。あなたのほかに３人の人間がいます。あなたは３人からキーワードをもらい、キーワードからより連想しやすいお題を応えます。テーマにあったお題が２つ出されました。テーマはフルーツ。お題は「りんご」と「梨」です。３人からのキーワードは「赤い」「iphone」「緑」でした。りんごと梨のどちらに近い？")
    return {"response": response.text}

app.include_router(router)