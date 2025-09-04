from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import torch
from torchvision import transforms
from PIL import Image
import io, os

app = FastAPI()

# Model load
MODEL_PATH = "./models/u2net.pth"
device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.load(MODEL_PATH, map_location=device)
model.eval()

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Transform for input image
transform = transforms.Compose([
    transforms.Resize((320, 320)),
    transforms.ToTensor()
])

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Preprocess
    input_tensor = transform(image).unsqueeze(0).to(device)

    # Predict mask
    with torch.no_grad():
        mask = model(input_tensor)[0][0].cpu().numpy()

    # Normalize mask
    mask = (mask - mask.min()) / (mask.max() - mask.min())
    mask_img = Image.fromarray((mask * 255).astype("uint8")).resize(image.size)

    # Apply mask to make background transparent
    rgba = image.convert("RGBA")
    datas = rgba.getdata()
    new_data = []
    mask_data = mask_img.getdata()

    for i, item in enumerate(datas):
        new_data.append((item[0], item[1], item[2], mask_data[i]))

    rgba.putdata(new_data)
    out_path = f"{OUTPUT_DIR}/{file.filename}_bg_removed.png"
    rgba.save(out_path, "PNG")

    return FileResponse(out_path, media_type="image/png", filename="bg_removed.png")

@app.get("/")
async def root():
    return {"msg": "BG Remover API with U²Net is running 🚀"}
