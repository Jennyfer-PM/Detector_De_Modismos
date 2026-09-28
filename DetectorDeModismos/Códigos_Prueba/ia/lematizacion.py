import spacy

nlp = spacy.load("es_core_news_lg")

texto_ejemplo = "Me cayó el veinte cuando iba caminando hacia mi casa"

documento = nlp(texto_ejemplo)

def lem_dic_mod(documento):
    for palabra in documento:
        print(palabra.text, "->", palabra.lemma_)

lem_dic_mod(documento)
