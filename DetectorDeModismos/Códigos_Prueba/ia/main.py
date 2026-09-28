from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cerebro import detector_modismos

app = FastAPI() 

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],              
)

@app.get("/")
def inicio():
    return ({"mensaje": "API funcionando"})

@app.post("/detectar")
def detectar(datos: dict):
    texto = datos["texto"]

    resultado = detector_modismos(texto, "detectar")

    return (resultado)

@app.post("/porcentaje")
def porcentaje(datos: dict):
    texto = datos["texto"]

    resultado = detector_modismos(texto, "porcentaje")

    return (resultado)


@app.post("/modismo")
def modismo(datos:dict):
    texto = datos["texto"]

    resultado = detector_modismos(texto, "modismo")

    return (resultado)

@app.post("/indices")
def indices(datos:dict):
    texto = datos["texto"]

    resultado = detector_modismos(texto, "indices")

    return (resultado)