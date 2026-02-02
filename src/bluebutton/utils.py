import os
import httpx
from dotenv import load_dotenv

load_dotenv()
_access_token: str | None = None

async def get_access_token() -> str:
    """Exchange client credentials for an access token."""
    global _access_token
    
    if _access_token is None:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                os.environ["TOKEN_URL"],
                data={
                    "grant_type": "client_credentials",
                    "client_id": os.environ["CLIENT_ID"],
                    "client_secret": os.environ["CLIENT_SECRET"],
                },
                timeout=30.0
            )
            response.raise_for_status()
            _access_token = response.json()["access_token"]
    
    return _access_token