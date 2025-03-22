from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf 
import numpy as np
from PIL import Image
import io
import asyncio
import time
import httpx


async def ping_app():
    url ="https://ai-model-te1d.onrender.com/ping"
    while True:
        try:
            async with httpx.AsyncClient() as client:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                response = await client.get(url)  # Update with your actual API URL
                print(f'{current_time}      :ping application')
        except Exception as error:
            print(error)
        await asyncio.sleep(30)



async def lifespan(app: FastAPI):
    task = asyncio.create_task(ping_app())
    yield
    task.cancel()


app = FastAPI( lifespan=lifespan)

origins =[
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = tf.keras.models.load_model("model.keras")
class_names = ["Healthy", "Infected"]

def predict_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB").resize((150, 150))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    confidence = prediction[0][0] * 100
    predicted_class = class_names[1 if prediction[0][0] > 0.5 else 0]

    return {"class": predicted_class, "confidence": f"{confidence:.2f}%"}


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = predict_image(image_bytes)
    return result

@app.get('/ping')
async def ping():
    return {"message": "pong"}