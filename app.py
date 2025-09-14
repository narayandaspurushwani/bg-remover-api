from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from rembg import remove
import io
from PIL import Image
import base64
import uvicorn

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    input_bytes = await file.read()
    output_bytes = remove(input_bytes)
    
    encoded_output = base64.b64encode(output_bytes).decode('utf-8')
    return JSONResponse(content={"image_base64": encoded_output})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
