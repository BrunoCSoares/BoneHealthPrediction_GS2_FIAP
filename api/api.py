import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
import tensorflow as tf
import numpy as np

app = FastAPI(title="BoneGuard Vision API")

# Redireciona a raiz para o Swagger automaticamente
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Carrega o modelo treinado
modelo = tf.keras.models.load_model('models/boneguard_modelo_v2.h5')
classes = ['Normal', 'Osteopenia', 'Osteoporosis']

@app.post("/analisar-radiografia")
async def analisar_raio_x(file: UploadFile = File(...)):
    conteudo = await file.read()
    caminho_temp = f"temp_{file.filename}"
    
    # Salva o arquivo temporariamente para usar o motor de leitura idêntico ao Colab
    with open(caminho_temp, "wb") as buffer:
        buffer.write(conteudo)
        
    try:
        # Leitura 100% idêntica ao treinamento
        img = tf.keras.utils.load_img(caminho_temp, target_size=(224, 224))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        
        # Inferência
        previsoes = modelo.predict(img_array)
        indice_classe = np.argmax(previsoes[0])
        confianca = float(np.max(previsoes[0]))
        
        # Retorno estruturado 
        return {
            "classificacao": classes[indice_classe],
            "confianca": round(confianca, 4),
            "probabilidades_brutas": {
                "Normal": round(float(previsoes[0][0]), 4),
                "Osteopenia": round(float(previsoes[0][1]), 4),
                "Osteoporosis": round(float(previsoes[0][2]), 4)
            }
        }
    finally:
        # Garante a exclusão do arquivo temporário
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)