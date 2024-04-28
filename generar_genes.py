import csv
import random

# leer periodos de UDF.csv
def leer_periodos():
    periodos = {}
    with open('UDF.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            periodos[row['Clave']] = [row['P1'], row['P2'], row['P3']]
    return periodos

# leer profesores y materias de Profesores y Materias.csv
def leer_profesores_materias():
    profesores_materias = {}
    with open('Profesores y Materias.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #Victor Manion,Juan Alvarado,Roberto Leyva,Mauricio Paletta,Yerly Flores,Jaime Lopez,Jorge Rodriguez,Jose Aguilera,Luis Guadarrama,Pedro Hernandez,Maria Mirafuentes,Roberto Vera,Octavio Silva,Fernando Ruiz,Ivan Olmos,Israel Tabarez
            profesores_materias[row['Clave']] = [row['Victor Manion'], row['Juan Alvarado'], row['Roberto Leyva'], row['Mauricio Paletta'], row['Yerly Flores'], row['Jaime Lopez'], row['Jorge Rodriguez'], row['Jose Aguilera'], row['Luis Guadarrama'], row['Pedro Hernandez'], row['Maria Mirafuentes'], row['Roberto Vera'], row['Octavio Silva'], row['Fernando Ruiz'], row['Ivan Olmos'], row['Israel Tabarez']]
    return profesores_materias

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
            # si el ultimo elemento de CLAVE no es B(bloque), agregar profesor en el archivo Profesores y Materias.csv
            if curso['CLAVE'][-1] != 'B':
                # open Profesores y Materias.csv
                for clave, profesor in profesores_materias.items():
                    if clave == curso['CLAVE']:
                        print(profesor)
                        # Add your code here to handle the 'profesor' variable

            gen = {'UF': [curso['CLAVE'], grupo], 
                   'Periodo': periodo}
            cromosoma.append(gen)

    # aleatorio de genes en el cromosoma
    random.shuffle(cromosoma)

    return cromosoma

# generar poblacion
#poblacion1 = [generar_cromosomas() for _ in range(100)]

# imprimir poblacion
# for i, cromosoma in enumerate(poblacion1, 1):
#     print(f"Cromosoma {i}:")
#     for curso in cromosoma:
#         print(curso)
#     print()

print(generar_cromosomas())