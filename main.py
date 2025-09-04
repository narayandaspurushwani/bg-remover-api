from fastapi import FastAPI, UploadFile, File
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Background Remover API is running!"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_image = Image.open(io.BytesIO(await file.read()))
    output_image = remove(input_image)
    byte_io = io.BytesIO()
    output_image.save(byte_io, "PNG")
    return {"status": "success", "msg": "Background removed!"}
