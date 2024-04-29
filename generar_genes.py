import csv
import random
from datetime import time

lista_profesor_materia = ['Victor Manion', 'Juan Alvarado', 'Roberto Leyva', 'Mauricio Paletta', 'Yerly Flores', 'Jaime Lopez', 'Jorge Rodriguez', 'Jose Aguilera', 'Luis Guadarrama', 'Pedro Hernandez', 'Maria Mirafuentes', 'Roberto Vera', 'Octavio Silva', 'Fernando Ruiz', 'Ivan Olmos', 'Israel Tabarez']
horario_profesor = {"Victor Manion": "Flexible", "Juan Alvarado": "Flexible", "Roberto Leyva": "Flexible", "Mauricio Paletta": "Flexible", "Yerly Flores": "Flexible", 
                    "Jaime Lopez": {"Lunes": [time(7,0), time(11,0)], "Martes": "NA", "Miercoles": [time(7,0), time(11,0)], "Jueves": [time(7,0), time(11,0)], "Viernes": "NA"},
                    "Jorge Rodriguez": {"Lunes": "NA", "Martes": "NA", "Miercoles": [time(7,0), time(10,0)], "Jueves": "NA", "Viernes": "NA"},
                    "Jose Aguilera": {"Lunes": [time(9, 0), time(13, 0), time(17, 0), time(20, 0)], "Martes": "NA", "Miercoles": [time(9, 0), time(13, 0), time(17, 0), time(20, 0)], "Jueves": "NA", "Viernes": [time(9, 0), time(13, 0), time(17, 0), time(20, 0)]}, 
                    "Luis Guadarrama": {"Lunes": [time(7,0), time(9,0)], "Martes": [time(7,0), time(9,0)], "Miercoles": [time(7,0), time(9,0)], "Jueves": [time(7,0), time(9,0)], "Viernes": [time(7,0), time(9,0)]}, 
                    "Pedro Hernandez": {"Lunes": [time(11,0), time(21,0)], "Martes": [time(11,0), time(21,0)], "Miercoles": [time(11,0), time(21,0)], "Jueves": [time(11,0), time(21,0)], "Viernes": [time(11,0), time(21,0)]},
                    "Maria Mirafuentes": {"Lunes": "NA", "Martes": "NA", "Miercoles": "NA", "Jueves": "NA", "Viernes": [time(11,0), time(13,0), time(15,0), time(17,0)]}, 
                    "Roberto Vera": {"Lunes": [time(11,0), time(21,0)], "Martes": [time(11,0), time(21,0)], "Miercoles": [time(11,0), time(21,0)], "Jueves": [time(11,0), time(21,0)], "Viernes": [time(11,0), time(21,0)]},
                    "Octavio Silva": ["Flexible"], 
                    "Fernando Ruiz": ["Flexible"], 
                    "Ivan Olmos": {"Lunes": [time(17,0), time(19,0)], "Martes": "NA", "Miercoles": [time(17,0), time(19,0)], "Jueves": "NA", "Viernes": "NA"},
                    "Israel Tabarez": "Flexible"}

# leer periodos de UDF.csv
def leer_periodos():
    periodos = {}
    with open('UDF.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            periodos[row['Clave']] = [row['P1'], row['P2'], row['P3']]
    return periodos
# El resultado es un diccionario con las claves de los cursos y los periodos disponibles

# leer profesores y materias de Profesores y Materias.csv
def leer_profesores_materias():
    profesores_materias = {}
    with open('Profesores y Materias.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            profesores_materias[row['Clave']] = [row['Victor Manion'], row['Juan Alvarado'], row['Roberto Leyva'], row['Mauricio Paletta'], row['Yerly Flores'], row['Jaime Lopez'], row['Jorge Rodriguez'], row['Jose Aguilera'], row['Luis Guadarrama'], row['Pedro Hernandez'], row['Maria Mirafuentes'], row['Roberto Vera'], row['Octavio Silva'], row['Fernando Ruiz'], row['Ivan Olmos'], row['Israel Tabarez']]
    return profesores_materias
# El resultado es un diccionario con las claves de los cursos y los profesores disponibles

def leer_bloques(file):
    profesores_bloques = {}
    with open(file, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            profesores_bloques[row['Tema']] = [row['Victor Manion'], row['Juan Alvarado'], row['Roberto Leyva'], row['Mauricio Paletta'], row['Yerly Flores'], row['Jaime Lopez'], row['Jorge Rodriguez'], row['Jose Aguilera'], row['Luis Guadarrama'], row['Pedro Hernandez'], row['Maria Mirafuentes'], row['Roberto Vera'], row['Octavio Silva'], row['Fernando Ruiz'], row['Ivan Olmos'], row['Israel Tabarez']]
    return profesores_bloques



def generar_cromosomas():
    cromosoma = []

    periodos = leer_periodos()
    profesores_materias = leer_profesores_materias()

    # leer CSV
    cursos = []
    with open('Febrero-Junio.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursos.append({'CLAVE': row['CLAVE'], '# GPOs': int(row['# GPOs'])})

    # generar cantidad de grupos por curso
    for curso in cursos:
        # generar grupos
        for i in range(curso['# GPOs']):
            grupo = i + 1

            # periodos
            periodos_curso = periodos[curso['CLAVE']]
            print(periodos_curso)
            periodos_disponibles = []
            for j, periodo in enumerate(periodos_curso):
                if periodo == 'X':
                    periodos_disponibles.append(f'P{j+1}')
            periodo = ','.join(periodos_disponibles) if periodos_disponibles else 'N/A'

            # agregar profesor
            # si el clave del curso esta en el diccionario de profesores_materias
            if curso['CLAVE'] in profesores_materias:
                profesor_disponible = []
                hora_inicio = []
                hora_fin = []

                for j, profesor in enumerate(profesores_materias[curso['CLAVE']]):
                    if profesor == 'X':
                        # obtener nombre del profesor de la lista de profesores
                        profesor_disponible.append(lista_profesor_materia[j])
                profesor = random.choice(profesor_disponible) if profesor_disponible else 'N/A'
                UF = curso['CLAVE']
                
                #horarios del profesor
                horario = horario_profesor[profesor]
                if horario == "Flexible":
                    #horario de lunes a viernes de 7:00 a 21:00 aleatorio cada dia
                    #Hora inicio: [L,M,M,J,V] , Hora fin: [L,M,M,J,V]
                    hora_inicio = [
                        time(random.randint(7, 19), 0).strftime("%H:%M"),
                        time(random.randint(7, 19), 0).strftime("%H:%M"),
                        time(random.randint(7, 19), 0).strftime("%H:%M"),
                        time(random.randint(7, 19), 0).strftime("%H:%M"),
                        time(random.randint(7, 19), 0).strftime("%H:%M")
                    ]

                    #hora fin es la hora de inicio + 2-4 horas aleatorios, no puede ser mayor a 21:00
                    hora_fin = [
                        time(min(int(hora_inicio[0].split(":")[0]) + random.randint(2, 4), 21), 0).strftime("%H:%M"),
                        time(min(int(hora_inicio[1].split(":")[0]) + random.randint(2, 4), 21), 0).strftime("%H:%M"),
                        time(min(int(hora_inicio[2].split(":")[0]) + random.randint(2, 4), 21), 0).strftime("%H:%M"),
                        time(min(int(hora_inicio[3].split(":")[0]) + random.randint(2, 4), 21), 0).strftime("%H:%M"),
                        time(min(int(hora_inicio[4].split(":")[0]) + random.randint(2, 4), 21), 0).strftime("%H:%M")
                    ]
                gen = {'UF': [UF, grupo], 
                    'Periodo': periodo, 
                    'Profesor': profesor,
                    'Hora_inicio': hora_inicio,
                    'Hora_fin': hora_fin
                    }  
                cromosoma.append(gen)

            else:
                # si es un bloque, busca y abre el archivo correspondiente    -------------bloque------------
                profesor_disponible = []
                hora_inicio = []
                hora_fin = []
                profesores_bloques = leer_bloques(curso['CLAVE'] + '-Profesores.csv')
                
                # generar un gen para cada tema del bloque
                for i, tema in enumerate(profesores_bloques):
                    # Verificar si el tema no está vacío
                    if tema:
                        # Incrementar el número de grupo en cada iteración
                        #grupo = i + 1
                        
                        profesor_disponible = []
                        for j, profesor in enumerate(profesores_bloques[tema]):
                            if profesor == 'X':
                                # obtener nombre del profesor de la lista de profesores
                                profesor_disponible.append(lista_profesor_materia[j])
                        profesor = random.choice(profesor_disponible) if profesor_disponible else 'N/A'
                        UF = curso['CLAVE'] + '-' + tema

                        #horarios del profesor
                        horario = horario_profesor[profesor]
                        if horario == "Flexible":
                            #horario de lunes a viernes de 7:00 a 21:00 aleatorio cada dia
                            #Hora inicio: [L,M,M,J,V] , Hora fin: [L,M,M,J,V]
                            hora_inicio = [
                                time(random.randint(7, 19), 0).strftime("%H:%M"),
                                time(random.randint(7, 19), 0).strftime("%H:%M"),
                                time(random.randint(7, 19), 0).strftime("%H:%M"),
                                time(random.randint(7, 19), 0).strftime("%H:%M"),
                                time(random.randint(7, 19), 0).strftime("%H:%M")
                            ]

                            #hora fin es la hora de inicio + 2-4 horas aleatorios, no puede ser mayor a 21:00
                            hora_fin = [
                                time(min(int(hora_inicio[0].split(":")[0]) + random.randint(2, 4), 21), 0).strftime("%H:%M"),
                                time(min(int(hora_inicio[1].split(":")[0]) + random.randint(2, 4), 21), 0).strftime("%H:%M"),
                                time(min(int(hora_inicio[2].split(":")[0]) + random.randint(2, 4), 21), 0).strftime("%H:%M"),
                                time(min(int(hora_inicio[3].split(":")[0]) + random.randint(2, 4), 21), 0).strftime("%H:%M"),
                                time(min(int(hora_inicio[4].split(":")[0]) + random.randint(2, 4), 21), 0).strftime("%H:%M")
                            ]
                        
                        gen = {'UF': [UF, grupo], 
                            'Periodo': periodo, 
                            'Profesor': profesor,
                            'Hora_inicio': hora_inicio,
                            'Hora_fin': hora_fin
                            }
                        cromosoma.append(gen)

    # aleatorio de genes en el cromosoma
    #random.shuffle(cromosoma)
    return cromosoma

# generar poblacion
#poblacion1 = [generar_cromosomas() for _ in range(100)]

# imprimir poblacion
# for i, cromosoma in enumerate(poblacion1, 1):
#     print(f"Cromosoma {i}:")
#     for curso in cromosoma:
#         print(curso)
#     print()

cromosomas = generar_cromosomas()
for i in range(0, len(cromosomas)):
    print(cromosomas[i])