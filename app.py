from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from gradio_client import Client
import nest_asyncio
import base64
import uvicorn

nest_asyncio.apply()
app = FastAPI()

client = Client("NDPDevloper/RMBG")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        # base64 encode karke string me convert karo
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        result = client.predict([image_b64], api_name="/predict")
        return JSONResponse(content={"processed_image": result[0]})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
