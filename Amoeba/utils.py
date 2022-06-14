class Coltivazione:
    def __init__(self, nome, nomelatino, morfologia, link, caratteristicheAmbientali = None, comment = None, thumbnail = None):
        self.nome = nome
        self.nomelatino = nomelatino
        self.morfologia = morfologia
        self.link = link
        self.caratteristicheAmbientali = caratteristicheAmbientali
        self.comment = comment
        self.thumbnail = thumbnail


class CaratteristicheAmbientali:
    def __init__(self, caratteristicheClimatiche, caratteristicheSuolo):
        self.caratteristicheClimatiche = caratteristicheClimatiche
        self.caratteristicheSuolo = caratteristicheSuolo


class CaratteristicheClimatiche:
    def __init__(self, precipitazioni, temperatura, gradoUmidità):
        self.precipitazioni = precipitazioni
        self.temperatura = temperatura
        self.gradoUmidità = gradoUmidità


class Precipitazioni:
    def __init__(self, precipitazioniMin = None, precipitazioniMax = None):
        self.precipitazioniMin = precipitazioniMin
        self.precipitazioniMax = precipitazioniMax


class Temperatura:
    def __init__(self, temperaturaMin = None, temperaturaMax = None):
        self.temperaturaMin = temperaturaMin
        self.temperaturaMax = temperaturaMax


class CaratteristicheSuolo:
    def __init__(self, pendenza, altitudine, drenaggio, fertilità, tessitura):
        self.pendenza = pendenza
        self.altitudine = altitudine
        self.drenaggio = drenaggio
        self.fertilità = fertilità
        self.tessitura = tessitura


class Citta:
    def __init__(self, nome, lat = None, long = None, link = None):
        self.nome = nome
        self.lat = lat
        self.long = long
        self.link = link


class Territorio:
    def __init__(self, latitudine, longitudine, locazione, caratteristicheAmbientali = None):
        self.lat = latitudine
        self.long = longitudine
        self.locazione = locazione
        self.caratteristicheAmbientali = caratteristicheAmbientali
    



