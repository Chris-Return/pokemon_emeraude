from src.data.playerdata import *
import re

class DialogVariables():


    variables = {
        "name" : "PlayerData.name"
    }

    @staticmethod
    def replacer(match):
        key = match.group(1)
        value = str(DialogVariables.variables.get(key, f"%{key}"))
        return eval(value)

    @staticmethod
    def get_variable(texte):
        texte_sortie = re.sub(r"%(\w+)", DialogVariables.replacer, str(texte))
        return texte_sortie