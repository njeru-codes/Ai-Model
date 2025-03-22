from fastapi import FastAPI, File, UploadFile
import tensorflow as tf 
import numpy as np
from PIL import Image
import io



app = FastAPI()

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