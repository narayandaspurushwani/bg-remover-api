from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
import io, os

app = FastAPI()

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Background remove
    output_image = remove(input_image)

    out_path = f"{OUTPUT_DIR}/{file.filename}_bg_removed.png"
    output_image.save(out_path, "PNG")

    return FileResponse(out_path, media_type="image/png", filename="bg_removed.png")

@app.get("/")
async def root():
    return {"msg": "BG Remover API (default rembg) is running 🚀"}
