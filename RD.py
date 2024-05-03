import random
from datetime import time
from datetime import datetime
from datetime import time, timedelta

from generar_genes import generar_cromosomas

import csv
# No se pueden programar grupos en la franja que va desde las 13:00 hasta las 15:00 horas de lunes a viernes.
# Definir el rango de tiempo a verificar (de 13:00 a 15:00)
inicio_verificar = "13:00"
fin_verificar = "15:00"


def verificar_solapamientos_cromosoma(cromosoma, inicio_verificar, fin_verificar):
    penalizaciones = 0

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
                penalizaciones += random.uniform(9.1, 10.1)
    if penalizaciones != 0:
        return 1
    else:
        return 0


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
            penalizaciones += random.uniform(9.1, 10.1)

        # Verificar que los miércoles (posición 2) no tengan horas
        elif i == 2 and (inicio != time(0, 0) or final != time(0, 0)):
            penalizaciones += random.uniform(9.1, 10.1)
    if penalizaciones != 0:
        return 1
    else:
        return 0


############################################################################################################

def revisar_horarios_colision(diccionarios):
    horarios_profesores = {}
    pen = 0

    for diccionario in diccionarios:
        uf = diccionario['UF'][0]
        profesor = diccionario['Profesor']
        horario_inicio = diccionario['Hora_inicio']
        horario_fin = diccionario['Hora_fin']

        # Si el profesor ya está en el diccionario de horarios
        if profesor in horarios_profesores:
            for dia in range(5):  # 0 representa lunes, 1 martes, ..., 4 viernes
                for uf_guardada, horarios_uf_guardada in horarios_profesores[profesor].items():
                    if uf != uf_guardada:
                        for horario_guardado in horarios_uf_guardada[dia]:
                            # Revisar si hay conflicto de horarios para cada día
                            if (horario_inicio[dia] < horario_guardado[1] and horario_inicio[dia] >= horario_guardado[0]) or \
                               (horario_fin[dia] > horario_guardado[0] and horario_fin[dia] <= horario_guardado[1]):
                                #print(f"Conflicto de horario para el profesor {profesor} en las UFs {uf} y {uf_guardada}, el día {dia + 1}: {horario_inicio[dia]}-{horario_fin[dia]} coincide con {horario_guardado[0]}-{horario_guardado[1]}")
                                pen = 1
                                break
                else:
                    # No hay conflicto de horarios, agregar el nuevo horario para este día
                    if profesor in horarios_profesores and uf in horarios_profesores[profesor]:
                        horarios_profesores[profesor][uf][dia].append((horario_inicio[dia], horario_fin[dia]))
                    else:
                        horarios_profesores.setdefault(profesor, {}).setdefault(uf, [[(horario_inicio[i], horario_fin[i])] for i in range(5)])
        else:
            # El profesor no está en el diccionario, agregarlo con sus horarios para cada día
            horarios_profesores[profesor] = {uf: [[(horario_inicio[i], horario_fin[i])] for i in range(5)]}

    #print("Revisión de horarios completada.")
    return pen

############################################################################################################

import csv

def contabilizar_horas(diccionarios):
    horas_por_uf = {}
    for diccionario in diccionarios:
        clave_uf, grupo = diccionario['UF']  # Acceder a la clave y al grupo de la UF
        horas_totales = 0
        horario_inicio = diccionario['Hora_inicio']
        horario_fin = diccionario['Hora_fin']

        for dia in range(5):  # Lunes a viernes
            hora_inicio = horario_inicio[dia]
            hora_fin = horario_fin[dia]

            if hora_inicio != '00:00' and hora_fin != '00:00':  # Verificar si hay horario para este día
                # Calcular las horas para este día
                horas_dia = (int(hora_fin[:2]) - int(hora_inicio[:2])) + (int(hora_fin[3:]) - int(hora_inicio[3:])) / 60
                horas_totales += horas_dia

        clave_grupo = (clave_uf, grupo)
        if clave_grupo in horas_por_uf:
            horas_por_uf[clave_grupo] += horas_totales
        else:
            horas_por_uf[clave_grupo] = horas_totales

    return horas_por_uf

def revisar_horas_excedidas(diccionarios, archivo_csv):
    horas_por_uf=contabilizar_horas(diccionarios)
    pen=0
    with open(archivo_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            clave_uf_csv = row['ï»¿Clave'].strip()  # Eliminar espacios en blanco alrededor de la clave de la UF
            horas_csv = float(row['Horas'])
            for clave_uf, horas_contadas in horas_por_uf.items():
                if clave_uf[0] == clave_uf_csv:
                    if horas_contadas > horas_csv:
                        print(f"¡Alerta! Horas excedidas para la UF {clave_uf[0]}, grupo {clave_uf[1]}. Horas contadas: {horas_contadas}, horas permitidas: {horas_csv}")
                        pen=1
    return pen


def revisar_disponibilidad_profesores(diccionarios, archivo_csv):
    pen=0
    with open(archivo_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for diccionario in diccionarios:
            uf_clave = diccionario['UF'][0]
            profesor = diccionario['Profesor']
            

            for row in reader:
                
                if row['Clave'].strip() == uf_clave and row[profesor] == 'X':
                    break
                elif row['Clave'].strip() == uf_clave and row[profesor] != 'X':
            
                    print(f"¡Alerta! El profesor {profesor} no está disponible para dar clases en la UF {uf_clave}.")
                    pen=1
    return pen



############################################################################################################

# Una clase no puede iniciar en horas pares, a menos que la hora impar inmediatamente superior ya haya sido asignada a otro profesor.

def hora_impar_superior(hora):
    # Obtiene la hora en formato de 24 horas y devuelve la próxima hora impar
    hora_dt = datetime.strptime(hora, "%H:%M")
    siguiente_hora = hora_dt + timedelta(hours=1)
    if siguiente_hora.hour % 2 == 0:  # Si es par, avanza una hora más
        siguiente_hora += timedelta(hours=1)
    return siguiente_hora.strftime("%H:%M")


def validar_horario(cursos):
    penalizacion = 0
    for curso in cursos:
        horas_inicio = curso["Hora_inicio"]
        bloque = curso["UF"]  # Suponiendo que "UF" indica el bloque del curso
        profesor = curso["Profesor"]

        for hora_inicio in horas_inicio:
            # Verificar si la hora de inicio es par
            if hora_inicio[-2:] == "00":
                hora_impar_superior_actual = hora_impar_superior(hora_inicio)

                # Verificar si la hora impar superior está asignada a otro profesor
                hora_impar_superior_asignada = False
                for otro_curso in cursos:
                    if (
                        otro_curso["UF"] == bloque
                        and otro_curso["Profesor"] != profesor
                    ):
                        if hora_impar_superior_actual in otro_curso["Hora_inicio"]:
                            hora_impar_superior_asignada = True
                            break

                # Si la hora impar superior está asignada, imprimir mensaje
                if hora_impar_superior_asignada:
                    penalizacion += random.uniform(9.1, 10.1)
                else:
                    penalizacion = 0
            else:
                penalizacion = 0
    if penalizacion != 0:
        return 1
    else:
        return 0



# Genera la población
file1 = "Agosto-Diciembre.csv"
poblacion1 = [generar_cromosomas(file1) for _ in range(5)]

# Evaluar la población
penalizaciones = []  # Initialize an empty list for penalizaciones
for cromosoma in poblacion1:
    penalizacion =  revisar_disponibilidad_profesores(cromosoma,"Profesores y Materias.csv")
    penalizaciones.append(penalizacion)  # Append the penalization value to the list
    #print("cronosoma:", cromosoma)
    print("Penalizaciones:", penalizacion)
    print("")

#penalizacion total de la poblacion
penalizaciones_poblacion = sum(penalizaciones)
print("Penalizaciones:", penalizaciones_poblacion)

