from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uuid
import os
from rembg import remove
from PIL import Image

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    # Save uploaded file
    file_name = f"{uuid.uuid4()}.png"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Remove background
    input_image = Image.open(file_path)
    output_image = remove(input_image)
    output_path = os.path.join(OUTPUT_DIR, file_name)
    output_image.save(output_path)

    return FileResponse(output_path, media_type="image/png")
