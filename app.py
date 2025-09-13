from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from gradio_client import Client
import nest_asyncio

nest_asyncio.apply()
app = FastAPI()

client = Client("NDPDevloper/RMBG")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = client.predict([image_bytes], api_name="/predict")
    return JSONResponse(content={"processed_image": result[0]})
