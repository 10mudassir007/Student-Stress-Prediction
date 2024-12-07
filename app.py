from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import os
import pickle
import numpy as np
import warnings

# Initialize FastAPI app
app = FastAPI()

# Suppress warnings
warnings.filterwarnings('ignore')

# Initialize Jinja2 template engine
templates = Jinja2Templates(directory="templates")

# Define the request body model using Pydantic
class PredictionRequest(BaseModel):
    study_hours: float
    extracrr_hours: float
    sleep_hours: float
    social_hours: float
    phy_activity: float
    gpa: float

# Prediction function (directly integrated into the endpoint)
@app.post("/predict/")
async def predict(data: PredictionRequest):
    # Prepare input data as a numpy array
    array = np.array([[data.study_hours, data.extracrr_hours, data.sleep_hours, data.social_hours, data.phy_activity, data.gpa]]).reshape(1, -1)

    # Load scaler and model
    with open("scaler.pkl", 'rb') as f:
        sc = pickle.load(f)
    with open("svm_model.pkl", 'rb') as f:
        svm = pickle.load(f)

    # Scale the input data
    array = sc.transform(array)

    # Make the prediction
    pred = svm.predict(array)
    
    # Return the prediction result
    if pred == 0:
        return {"prediction": "Low"}
    elif pred == 1:
        return {"prediction": "Moderate"}
    elif pred == 2:
        return {"prediction": "High"}

# Serve static files (CSS, JS, images) from the templates folder
@app.get("/static/{file_name}")
async def serve_static(file_name: str):
    file_path = os.path.join("templates", file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#array([[5.  , 1.7 , 7.6 , 0.3 , 9.4 , 2.53]])