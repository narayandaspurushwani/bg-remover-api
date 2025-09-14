from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from rembg import remove
import base64
# Import the CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the BG Remover API. Use the /remove-bg/ endpoint to remove backgrounds from images. You can find the documentation at /docs"}

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    output_bytes = remove(image_bytes)
    encoded_img = base64.b64encode(output_bytes).decode('utf-8')
    return JSONResponse(content={
        "processed_image": f"data:image/png;base64,{encoded_img}"
    })
