from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.analytics import create_mock_api, get_mock_api_response

# Create FastAPI app instance
app = FastAPI()

@app.get("/")
def health_check():
    return {"message": "API is running"}

@app.get("/mock/{api_name}")
def mock_api(api_name: str, user_id: int = None, name: str = None, activity: str = None):
    # Get mock API response based on query parameters
    try:
        response = get_mock_api_response(api_name, user_id=user_id, name=name, activity=activity)
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=404, detail="API not found")

@app.post("/mock/{api_name}")
def create_api(api_name: str, method: str, response_template: str):
    # Create a new mock API
    try:
        create_mock_api(api_name, method, response_template)
        return {"message": "API created successfully", "api_name": f"mock/{api_name}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error creating API")
