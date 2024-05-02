import random
from datetime import time
from datetime import datetime
from datetime import time, timedelta

# No se pueden programar grupos en la franja que va desde las 13:00 hasta las 15:00 horas de lunes a viernes.
# Definir el rango de tiempo a verificar (de 13:00 a 15:00)
inicio_verificar = "13:00"
fin_verificar = "15:00"


def verificar_solapamientos_cromosoma(cromosoma, inicio_verificar, fin_verificar):
    coincidencias = 0

    # Convertir los horarios de verificación a objetos de tiempo
    inicio_verificar = datetime.strptime(inicio_verificar, "%H:%M").time()
    fin_verificar = datetime.strptime(fin_verificar, "%H:%M").time()

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

            # Verificar si hay solapamiento entre los intervalos
            if inicio < fin_verificar and final > inicio_verificar:
                coincidencias += random.uniform(9.1, 10.1)

    return coincidencias


######################################################################
# Las materias se deben programar en no más de dos horas diarias y en los pares de días lunes-jueves o martes-viernes.

# Verificación de las horas
def verificar_horas(cromosoma):
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

        # Calcular la diferencia de tiempo entre hora de inicio y fin
        diferencia = timedelta(hours=final.hour, minutes=final.minute) - timedelta(
            hours=inicio.hour, minutes=inicio.minute
        )

        # Ignorar si ambos son time(0, 0), que representa sin horas para ese día
        if inicio == time(0, 0) and final == time(0, 0):
            continue

        # Verificar si la diferencia es exactamente de 2 horas
        elif diferencia != timedelta(hours=2):
            penalizaciones += 1

        # Verificar que los miércoles (posición 2) no tengan horas
        elif i == 2 and (inicio != time(0, 0) or final != time(0, 0)):
            penalizaciones += 1

    return penalizaciones


####################################################################################3
#Una clase no puede iniciar en horas pares, a menos que la hora impar inmediatamente superior ya haya sido asignada a otro profesor.

""""
# Verificación de las horas
def verificar_horas_pares(cromosoma):
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

        if horas_inicio.hour % 2 == 0:
            penalizaciones += 1

    return penalizaciones
    """