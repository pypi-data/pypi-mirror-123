from assignmentcalculatorunimib.op import crea_array, scelta_operatore


def main():
    value_1_1 = 3
    value_1_2 = 4
    value_1_3 = 5

    value_2_1 = 2
    value_2_2 = 6
    value_2_3 = 9

    operatore = "somma"

    array_1 = crea_array(value_1_1, value_1_2, value_1_3)
    array_2 = crea_array(value_2_1, value_2_2, value_2_3)

    esito, risposta = scelta_operatore(operatore, array_1, array_2)
    if esito:
        print(risposta)
    else:
        print("errore operatore")
