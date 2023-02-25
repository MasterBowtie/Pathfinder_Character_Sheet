

class Ancestry:
    def __init__(self, ancestry: dict, name: str):
        self.__name = name
        self.__ancestry = ancestry
        #self.__heritage = heritage

    def getAncestry(self):
        return self.__name

    def getSource(self):
        return self.__ancestry["source"]

    def getTraits(self):
        return self.__ancestry["trait"]

    def getDescription(self):
        return self.__ancestry["description"]

    def getHP(self):
        return self.__ancestry["hp"]

    def getSize(self):
        return self.__ancestry["size"]

    def getBoosts(self):
        return self.__ancestry["boosts"]

    def getFlaws(self):
        return self.__ancestry["flaws"]

    def getLanguages(self):
        return self.__ancestry["languages"]

    def getAdditionalLanguages(self):
        return self.__ancestry["addLanguages"]

    def getExtras(self):
        return self.__ancestry["extras"]

    def setBoost(self, score: str):
        #TODO: setup for Free exchange
        pass

    def setAncestry(self, ancestry: dict):
        self.__ancestry = ancestry
