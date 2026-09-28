import json
import spacy
from thefuzz import fuzz
from pathlib import Path

ruta_json = Path(__file__).parent.parent / "data" / "modismos.json"

with open(ruta_json, "r", encoding="utf-8") as archivo:
    modismos = json.load(archivo)

ruta_json = Path(__file__).parent.parent / "data" / "modismospatron.json"

with open(ruta_json, "r", encoding="utf-8") as archivo:
    modismospatron = json.load(archivo)

nlp = spacy.load("es_core_news_lg")

def detectado_parcial(texto):
    encontrados = []
    lematizados = []
    porcentajes = []

    documento = nlp(texto)
    
    for palabra in documento:
        lematizados.append(palabra.lemma_)

    for modismo in modismospatron:
        elementos_comun = set(modismo["patron"]) & set(lematizados)

        if len(elementos_comun) >= round(len(modismo["patron"]) / 2):

            encontrados.append(modismo["modismo"])

            ecjunto = " ".join(elementos_comun)
            locjunta = " ".join(lematizados)
            patjunto = " ".join(modismo["patron"])
            porcentajefrase = fuzz.ratio(locjunta, patjunto)
            porcentajeelementos = fuzz.ratio(ecjunto, patjunto)

            #print("Porcentaje frase completa: ", porcentajefrase)
            #print("Porcentaje solo elementos: ", porcentajeelementos)

            porcentaje_completo = ((porcentajefrase + porcentajeelementos) / 2)

            porcentajes.append(porcentaje_completo)

        promedioP = sum(porcentajes) / len(porcentajes)

    return promedioP
        #resultado = "\nFrase: ", documento, "Porcentaje de coincidencia con modismos: ", porcentajes, "%", "El o los modismos que se estan utilizando son: \n", encontrados

"""detectado_parcial("Ana y yo estabamos tan en la luna cuando nos fuimos de pinta que ni cuenta nos dimos que ese dia teniamos examen hasta que nos cayo bien feo el veinte")
detectar_modismos("Ana y yo estabamos tan en la luna cuando nos fuimos de pinta que ni cuenta nos dimos que ese dia teniamos examen hasta que nos cayo bien feo el veinte")

detectado_parcial("Ya me cayo bien feo el veinte")
detectar_modismos("Ya me cayo bien feo el veinte")

detectado_parcial("Ya me cayó bien feo el veinte")
detectar_modismos("Ya me cayó bien feo el veinte")"""