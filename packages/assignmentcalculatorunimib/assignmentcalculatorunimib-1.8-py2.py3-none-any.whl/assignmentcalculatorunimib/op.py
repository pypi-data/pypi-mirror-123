import numpy as np

from assignmentcalculatorunimib.calculator import somma, sottrazione


def scelta_operatore(operatore, array_1, array_2):
    if operatore == "somma":
        return True, somma(array_1, array_2)
    if operatore == "sottrazione":
        return True, sottrazione(array_1, array_2)
    return False, -1


def crea_array(value_1, value_2, value_3):
    return np.array([value_1, value_2, value_3])
