from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Background Remover API is running!"}

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    # File ko read karna
    contents = await file.read()

    # Background remove karna
    input_image = Image.open(io.BytesIO(contents))
    output_image = remove(input_image)

    # Convert output into bytes
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")
