from fastapi import FastAPI, HTTPException, Header
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_KEY = os.getenv("API_KEY")

@app.get("/get-token")
async def get_token(api_key: str = Header(None)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    try:
        response = requests.post(
            "https://dev.abdm.gov.in/gateway/v0.5/sessions",
            json={"clientId": CLIENT_ID, "clientSecret": CLIENT_SECRET}
        )
        response.raise_for_status()
        access_token = response.json().get("accessToken")
        if not access_token:
            raise HTTPException(status_code=500, detail="No access token found in response")
        return {"accessToken": access_token}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
