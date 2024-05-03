import random
from datetime import time
from datetime import datetime
from datetime import time, timedelta

from generar_genes import generar_cromosomas


# En lo posible garantizar que los bloques tengan un horario continuo a lo largo de un día (no haya fracciones o segmentos).
def verificar_horarios_continuos(cromosoma):
    penalizaciones = 0

    # Iterar por cada curso en el cromosoma
    for curso in cromosoma:
        # Verificar si curso es una lista, si es así, convertirlo a un diccionario
        if isinstance(curso, list):
            curso = {
                "UF": curso[0],
                "Periodo": curso[1],
                "Profesor": curso[2],
                "Hora_inicio": curso[3],
                "Hora_fin": curso[4],
            }

        # Obtener los horarios de inicio y fin del curso
        horas_inicio = curso["Hora_inicio"]
        horas_fin = curso["Hora_fin"]

        # Verificar los horarios de cada día de la semana
        for i in range(5):
            inicio = datetime.strptime(horas_inicio[i], "%H:%M").time()
            final = datetime.strptime(horas_fin[i], "%H:%M").time()

        if final < inicio:
            penalizaciones += 1

        """# Verificar si los horarios son continuos
        if i > 0:
            # Obtener el final del día anterior
            final_anterior = hora_final['horarios'][i - 1]

            # Comparar la hora de inicio con el final anterior
            if inicio != final_anterior:
                penalizaciones += 1"""

    return penalizaciones

############################################################################################################
'''
# Genera la población
file1 = "Agosto-Diciembre.csv"
poblacion1 = [generar_cromosomas(file1) for _ in range(100)]

# Evaluar la población
penalizaciones = []  # Initialize an empty list for penalizaciones
for cromosoma in poblacion1:
    penalizacion = verificar_horarios_continuos(cromosoma)
    penalizaciones.append(penalizacion)  # Append the penalization value to the list
    print("cronosoma:", cromosoma)
    print("Penalizaciones:", penalizacion)
    print("")

# penalizacion total de la poblacion
penalizaciones_poblacion = sum(penalizaciones)
print("Penalizaciones:", penalizaciones_poblacion)
'''