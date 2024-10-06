from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from saas_calculation import final_result
import uvicorn

app = FastAPI()

# Configure CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/saas-metrics")
async def get_financial_metrics():
    result = final_result()
    print(result, type(result))
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
