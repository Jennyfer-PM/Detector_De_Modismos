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

def detectar_mod(texto):
    encontrados = []

    for modismo in modismos:
        if modismo["modismo"] in texto.lower():
            encontrados.append(modismo["modismo"])
    
    if encontrados == []:
        return modismos_lema(texto)
    else: return encontrados

def modismos_lema(texto):
    encontrados = []
    lematizados = []
    porcentajes = []

    documento = nlp(texto)
    
    for palabra in documento:
        lematizados.append(palabra.lemma_)
    
    #print(lematizados)

    for modismo in modismospatron:
        if set(modismo["patron"]).issubset(set(lematizados)):
            encontrados.append(modismo["modismo"])
            locjunta = " ".join(lematizados)
            #print(locjunta)
            patjunto = " ".join(modismo["patron"])
            #print(patjunto)
            #porcentaje_parcial = fuzz.partial_ratio(locjunta, patjunto)
            #coincidencia = (SequenceMatcher(None, locjunta, patjunto).ratio()) * 100
            porcentaje_completo = fuzz.ratio(locjunta, patjunto)

            porcentajes.append(porcentaje_completo)

    return print("Modismos detectados: ", encontrados, "\nPorcentaje de coincidencia: ", porcentajes)

modismos_lema(
    "El otro día me caí porque estaba en la luna"
)


"""detectar_modismos(
    "Estaba en la luna",
    modismos
)

detectar_modismos(
    "Juan y Carlos estaban en la luna desde hace media hora",
    modismos
)

detectar_modismos(
    "Mi familia no es muy grande, somos solo cuatro personas: mi padre, mi madre, mi hermana y yo. También tenemos un perro. Yo soy mayor que mi hermana, pero ella es más alta. Yo tengo doce años y ella once. Mis padres se llaman Javier y María, mi hermana se llama Sara y yo Luis. Vivimos todos juntos en una casa muy bonita.Mi padre es banquero y mi madre ama de casa. Por la mañana, desayunamos juntos en la cocina. Me gusta desayunar con mi familia. Además, por las mañanas siempre tengo hambre. Después del colegio, mi madre prepara una comida deliciosa. Por la tarde, mi madre queda con sus amigas, y mi padre juega al tenis. Mi hermana y yo hacemos los deberes, y después vemos la televisión. Los viernes por la tarde vamos los cuatro de compras. Mi padre es alto y rubio, y mi madre es morena y delgada. A mi hermana le gusta quedar con sus amigas en el parque. Yo me divierto mucho más jugando a los videojuegos en casa.",
    modismos
)

detectar_modismos(
    "Tu y yo nos fuimos de pinta el otro día no mientas",
    modismos
)

detectar_modismos(
    "Laura y Maria se habian ido de pinta el otro dia, estaban tan en la luna que hasta me lo confesaron",
    modismos
)"""