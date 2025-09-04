from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
from PIL import Image
import io

app = FastAPI()
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    out_path = f"{OUTPUT_DIR}/{file.filename}"
    image.save(out_path)  # TODO: Yaha background removal model lagana hai

    return FileResponse(out_path, media_type="image/png", filename="result.png")

@app.get("/")
async def root():
    return {"msg": "BG Remover API is running 🚀"}