import json 
import spacy
from pathlib import Path
from thefuzz import fuzz

ruta_json = Path(__file__).parent.parent / "data" / "patrones.json"

with open(ruta_json, "r", encoding="utf-8") as archivo:
    patrones = json.load(archivo)

nlp = spacy.load("es_core_news_lg")

def detector_modismos(texto, accion):
    modismos = []
    lematizados = []
    detectado = False
    indices_final = []
    indices_inicio = []
    indices = []
    i = 0
    #mod_lema = []
    lemas = []
    porcentajes = 0
    porcentaje_completo = 0
    indicesT = []

    documento = nlp(texto)

    for palabra in documento:
        lematizados.append(palabra.lemma_)

    for lem in lematizados:
        if lem == ",":
            lematizados.remove(",")
        elif lem == ".":
            lematizados.remove(".")
    
    limite = len(lematizados)

    #lemas_filtrados = [token.text for token in documento if not token.is_stop]}

    for patron in patrones:
        encontrados = set(patron["patron_s"]) & set(lematizados)

        if len(encontrados) > 0:
            for elemento_a in patron["patron_s"]:
                for elemento_c in lematizados:
                    if elemento_a == elemento_c:
                        indices_inicio.append(lematizados.index(elemento_c))
                    else: 
                        indices_inicio.append(limite)
        
        indices_inicio = list(set(indices_inicio))
        indices_inicio = sorted(indices_inicio)
        #print(indices_inicio)
        
        for indice in indices_inicio:
            #print(indice)
            #print(indices_inicio)
            if indice == limite:
                #print('estoy aqui')
                indices_inicio.remove(limite)
                #print(indices_inicio)
            else:
                if ((indice + 5) < limite): 
                    rango = lematizados[indice:(indice + 5)]
                else: rango = lematizados[indice:(limite)]

                #print(rango)

                for patron in patrones:
                    if patron["patron_p"] in rango:
                        mod = patron["modismo"]
                        if mod not in modismos: modismos.append(mod)
                        lemas.append(patron["lematizado"])
                        index = lematizados.index(patron["patron_p"])
                        if index not in indices_final: indices_final.append(index)
                        if indice not in indicesT: indicesT.append(indice)
                        for no in patron["no_detectar"]:
                            #print(no)
                            if no in lematizados:
                                modismos.remove(mod)
                                indices_final.remove(index)
                                indicesT.remove(indice)

            #print(indices_inicio)

            #contador += 1

        #print(detectado)
        #print(patron)
        #print(indices_inicio)
        #print(indicesT)

    indices_final = sorted(indices_final)
    indicesT = sorted(indicesT)

    if len(modismos) > 0:
        detectado = True

    #print(indices_inicio)
            
    if(detectado == True):        
        while i < len(indicesT):
            indices.append((indicesT[i], indices_final[i]))

            rango_modismo = lematizados[indicesT[i]:indices_final[i]+1]

            rango_junto = " ".join(rango_modismo)

            porcentaje = fuzz.ratio(rango_junto, (lemas[i]))

            porcentajes += porcentaje

            i = i + 1

        porcentaje_completo = porcentajes // i

    match accion:
        case "detectar":
            return detectado
        case "modismo":
            return modismos
        case "indices_i":
            return indices_inicio
        case "indices_f":
            return indices_final
        case "indices":
           return indices
        case "porcentaje":
           return porcentaje_completo

    

"""resultado1 = detector_modismos("El otro día me caí porque estaba en la luna", "detectar")
resultado2 = detector_modismos("El otro día me caí porque estaba en la luna", "modismo")
resultado3 = detector_modismos("El otro día me caí porque estaba en la luna", "indices")
resultado4 = detector_modismos("El otro día me caí porque estaba en la luna", "porcentaje")

print(resultado1)
print(resultado2)
print(resultado3)
print(resultado4)"""