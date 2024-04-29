import csv
import random

lista_profesor_materia = ['Victor Manion', 'Juan Alvarado', 'Roberto Leyva', 'Mauricio Paletta', 'Yerly Flores', 'Jaime Lopez', 'Jorge Rodriguez', 'Jose Aguilera', 'Luis Guadarrama', 'Pedro Hernandez', 'Maria Mirafuentes', 'Roberto Vera', 'Octavio Silva', 'Fernando Ruiz', 'Ivan Olmos', 'Israel Tabarez']
lista_bloque = ["TC1001B-Profesores.csv", "TC1002B-Profesores.csv", "TC1004B-Profesores.csv", "TC2005B-Profesores.csv", "TC2006B-Profesores.csv", "TC2007B-Profesores.csv", "TC2008B-Profesores.csv", "TC3002B-Profesores.csv", "TC3003B-Profesores.csv", "TC3004B-Profesores.csv", "TC3005B-Profesores.csv", "TI3005B-Profesores.csv"]

# leer periodos de UDF.csv
def leer_periodos():
    periodos = {}
    with open('UDF.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            periodos[row['Clave']] = [row['P1'], row['P2'], row['P3']]
    return periodos
# El resultado es un diccionario con las claves de los cursos y los periodos disponibles
# ['X', 'X', '']
# ['', 'X', '']
# ['X', '', '']
# ['', 'X', 'X']
# ['X', '', '']
# ['', 'X', '']
# ['', '', 'X']

# leer profesores y materias de Profesores y Materias.csv
def leer_profesores_materias():
    profesores_materias = {}
    with open('Profesores y Materias.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            profesores_materias[row['Clave']] = [row['Victor Manion'], row['Juan Alvarado'], row['Roberto Leyva'], row['Mauricio Paletta'], row['Yerly Flores'], row['Jaime Lopez'], row['Jorge Rodriguez'], row['Jose Aguilera'], row['Luis Guadarrama'], row['Pedro Hernandez'], row['Maria Mirafuentes'], row['Roberto Vera'], row['Octavio Silva'], row['Fernando Ruiz'], row['Ivan Olmos'], row['Israel Tabarez']]
    return profesores_materias
# El resultado es un diccionario con las claves de los cursos y los profesores disponibles
# ['X', '', '', 'X', '', '', '', '', '', '', '', '', '', '', '', '']
# ['', 'X', '', '', '', '', '', 'X', '', 'X', '', '', '', '', '', '']

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
                for j, profesor in enumerate(profesores_materias[curso['CLAVE']]):
                    if profesor == 'X':
                        # obtener nombre del profesor de la lista de profesores
                        profesor_disponible.append(lista_profesor_materia[j])
                profesor = random.choice(profesor_disponible) if profesor_disponible else 'N/A'
                UF = curso['CLAVE']

                gen = {'UF': [UF, grupo], 
                    'Periodo': periodo, 
                    'Profesor': profesor}  
                cromosoma.append(gen)

            else:
                # si es un bloque, busca y abre el archivo correspondiente
                profesor_disponible = []
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
                        
                        gen = {'UF': [UF, grupo], 
                            'Periodo': periodo, 
                            'Profesor': profesor}  
                        cromosoma.append(gen)

    # aleatorio de genes en el cromosoma
    # random.shuffle(cromosoma)
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