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

import csv

def obtener_semestre(uf, archivo_csv):
    with open(archivo_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row)
            if row['ï»¿Clave'] == uf:
                return int(row['Semestre'])
    return None

def revisar_horarios_semestres(diccionarios, archivo_csv):
    pen=0
    for diccionario in diccionarios:
        uf = diccionario['UF'][0]
        semestre = obtener_semestre(uf,"UDF.csv")
        if semestre in range(1, 6):
            profesor = diccionario['Profesor']
            horario_inicio = diccionario['Hora_inicio']
            horario_fin = diccionario['Hora_fin']

            for dia in range(5):  # Lunes a viernes
                # Verificar si el horario de inicio o fin es después de las 19:00
                if horario_inicio[dia] > '19:00' or horario_fin[dia] > '19:00':
                    #print(f"¡Alerta! El profesor {profesor} tiene una clase después de las 19:00 el día {dia + 1} en el semestre {semestre} para la UF {uf}.")
                    pen=1
    return pen
############################################################################################################
# Buscar que no haya clase los miércoles
def revisar_miercoles(cromosoma):
    pen=0
    for diccionario in cromosoma:
        hora_inicio = diccionario["Hora_inicio"]
        if hora_inicio[2] != "00:00":
            pen = 1
    return pen

# No asignar a un profesor más de 8 horas de clase por día
from datetime import datetime

def convertir_a_datetime(horas):
    # Convertir cada cadena de hora a un objeto datetime
    return [datetime.strptime(hora, '%H:%M') for hora in horas]

def verificar_duraciones(cromosoma):
    duraciones_por_profesor = {}

    # Calcular la duración de la clase para cada posición y actualizar el diccionario
    for clase in cromosoma:
        codigo_profesor = clase["Profesor"]
        hora_inicio = convertir_a_datetime(clase["Hora_inicio"])
        hora_fin = convertir_a_datetime(clase["Hora_fin"])
        duracion_clase = [(fin - inicio).seconds / 3600 for inicio, fin in zip(hora_inicio, hora_fin)]

        if codigo_profesor not in duraciones_por_profesor:
            duraciones_por_profesor[codigo_profesor] = [0] * len(duracion_clase)

        for i, duracion in enumerate(duracion_clase):
            duraciones_por_profesor[codigo_profesor][i] += duracion

    # Verificar que ninguna duración exceda las 8 horas por posición
    for profesor, duraciones in duraciones_por_profesor.items():
        for i, duracion in enumerate(duraciones):
            if duracion > 8:
                return 1

    return 0






















############################################################################################################

#Genera la población
file1 = "Agosto-Diciembre.csv"
poblacion1 = [generar_cromosomas(file1) for _ in range(2)]
print(poblacion1)

# Evaluar la población
penalizaciones = []  # Initialize an empty list for penalizaciones
for cromosoma in poblacion1:
    #penalizacion = revisar_horarios_semestres(cromosoma,"UDF.csv")
    penalizacion = verificar_duraciones(cromosoma)
    penalizaciones.append(penalizacion)  # Append the penalization value to the list
    #print("cronosoma:", cromosoma)
    print("Penalizaciones:", penalizacion)
    print("")

# penalizacion total de la poblacion
penalizaciones_poblacion = sum(penalizaciones)
print("Penalizaciones:", penalizaciones_poblacion)