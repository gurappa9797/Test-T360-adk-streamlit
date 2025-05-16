from fastapi import FastAPI, Request, Response
import httpx
import requests

ADK_BASE_URL = "http://localhost:8000"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/adk/sessions")
async def get_sessions():
    async with httpx.AsyncClient() as client:
        adk_response = await client.get(f"{ADK_BASE_URL}/apps/manager_agent/users/user/sessions")
        return Response(
            content=adk_response.content,
            status_code=adk_response.status_code,
            media_type=adk_response.headers.get("content-type")
        )

@app.post("/adk/run_sse")
async def post_run_sse(request: Request):
    data = await request.body()
    headers = {"content-type": request.headers.get("content-type", "application/json")}
    async with httpx.AsyncClient() as client:
        adk_response = await client.post(f"{ADK_BASE_URL}/run_sse", content=data, headers=headers)
        return Response(
            content=adk_response.content,
            status_code=adk_response.status_code,
            media_type=adk_response.headers.get("content-type")
        )
