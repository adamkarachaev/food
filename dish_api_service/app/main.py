import uvicorn
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/health")
async def service_alive():
    return {"message": "Service alive"}


@app.get("/search_food")
async def search_food(query: str):
    response = requests.get(
        f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&json=1")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="No products found")
    return response.json()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
