from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from rembg import remove
import base64

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    output_bytes = remove(image_bytes)
    encoded_img = base64.b64encode(output_bytes).decode('utf-8')
    return JSONResponse(content={
        "processed_image": f"data:image/png;base64,{encoded_img}"
    })
