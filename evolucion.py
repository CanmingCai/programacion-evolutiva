import numpy as np
import random
import csv
from generar_genes import generar_cromosomas
from costos import costo_cromosoma

lista_profesor_materia = ['Victor Manion', 'Juan Alvarado', 'Roberto Leyva', 'Mauricio Paletta', 'Yerly Flores', 'Jaime Lopez', 'Jorge Rodriguez', 'Jose Aguilera', 'Luis Guadarrama', 'Pedro Hernandez', 'Maria Mirafuentes', 'Roberto Vera', 'Octavio Silva', 'Fernando Ruiz', 'Ivan Olmos', 'Israel Tabarez']
periodos = [["P1,P2,P3"], ["P1,P2"], ["P2,P3"], ["P1"], ["P2"], ["P3"]]
UF =  ["TC1027", "TC1028", "TC1029", "TC1030", "TC1031", "TC1032", "TC1033", "TC2037", "TC2038", "TI1015"]
bloques = { "TC1001B": ["TC1001B-1", "TC1001B-2", "TC1001B-3", "TC1001B-4", "TC1001B-5", "TC1001B-6", "TC1001B-7"],
            "TC1002B": ["TC1002B-1", "TC1002B-2", "TC1002B-3", "TC1002B-4", "TC1002B-5", "TC1002B-6", "TC1002B-7"],
            "TC1004B": ["TC1004B-1", "TC1004B-2", "TC1004B-3", "TC1004B-4", "TC1004B-5", "TC1004B-6", "TC1004B-7", "TC1004B-8", "TC1004B-9"],
            "TC1005B": ["TC1005B-1", "TC1005B-2", "TC1005B-3", "TC1005B-4", "TC1005B-5", "TC1005B-6", "TC1005B-7", "TC1005B-8"],
            "TC1006B": ["TC1006B-1", "TC1006B-2", "TC1006B-3"],
            "TC1007B": ["TC1007B-1", "TC1007B-2", "TC1007B-3", "TC1007B-4", "TC1007B-5", "TC1007B-6"],
            "TC1008B": ["TC1008B-1", "TC1008B-2", "TC1008B-3", "TC1008B-4", "TC1008B-5", "TC1008B-6", "TC1008B-7"],
            "TC3002B": ["TC3002B-1", "TC3002B-2", "TC3002B-3", "TC3002B-4"],
            "TC3003B": ["TC3003B-1", "TC3003B-2", "TC3003B-3", "TC3003B-4"],
            "TC3004B": ["TC3004B-1", "TC3004B-2", "TC3004B-3", "TC3004B-4", "TC3004B-5"],
            "TC3005B": ["TC3005B-1", "TC3005B-2", "TC3005B-3", "TC3005B-4", "TC3005B-5", "TC3005B-6", "TC3005B-7"],
        }
# Genera la población
file1 = "Agosto-Diciembre.csv"
poblacion1 = [generar_cromosomas(file1) for _ in range(100)]

# evaluar el costo de los cromosomas 
costo = [costo_cromosoma(cromosoma) for cromosoma in poblacion1]
# Imprime el índice de la lista de costos
for i in range(len(costo)):
    print(i, costo[i])


def torneo_seleccion(poblacion, costo, cantidad=25):
    # Selecciona n cromosomas aleatorios
    selec_indices = np.random.choice(len(poblacion), cantidad, replace=False)
    selec_cromosomas = [poblacion[i] for i in selec_indices]
    
    # Encuentra el cromosoma con el costo mínimo entre los seleccionados
    min_costo_index = min(selec_indices, key=lambda x: costo[x])
    min_costo_cromosoma = poblacion[min_costo_index]
    min_costo = costo[min_costo_index]
    
    return selec_cromosomas, min_costo_cromosoma, min_costo


# Utiliza la función torneo_selection para seleccionar dos veces
selec_cromosomas_1, min_costo_cromosoma_1, min_cost_1 = torneo_seleccion(poblacion1, costo)
# Encuentra los índices de los cromosomas seleccionados en la población
selec_indices_1 = [poblacion1.index(cromosoma) for cromosoma in selec_cromosomas_1]

# Excluye los cromosomas seleccionados en la primera vez de la selección siguiente
indices_restantes = [i for i in range(len(poblacion1)) if i not in selec_indices_1]
selec_cromosomas_2, min_costo_cromosoma_2, min_costo_2 = torneo_seleccion([poblacion1[i] for i in indices_restantes], 
                                                                         [costo[i] for i in indices_restantes])
# Encuentra los índices de los cromosomas seleccionados en la población
selec_indices_2 = [indices_restantes[i] for i in range(len(selec_cromosomas_2))]

# Encuentra los índices de los dos cromosomas con el costo mínimo en la población
min_costo_index_1 = poblacion1.index(min_costo_cromosoma_1)
min_costo_index_2 = indices_restantes.index(poblacion1.index(min_costo_cromosoma_2)) if min_costo_cromosoma_2 in poblacion1 else -1

# print("Cromosomas seleccionados 1:")
# # Imprime los índices de los cromosomas seleccionados
# print(selec_indices_1)
# print("Índice del cromosoma con el costo mínimo 1:", min_costo_index_1)
# print("Cromosoma con el costo mínimo 1:", min_costo_cromosoma_1)
# print("Costo mínimo 1:", min_cost_1)

# print("Cromosomas seleccionados 2:")
# # Imprime los índices de los cromosomas seleccionados
# print(selec_indices_2)
# print("Índice del cromosoma con el costo mínimo 2:", min_costo_index_2)
# print("Cromosoma con el costo mínimo 2:", min_costo_cromosoma_2)
# print("Costo mínimo 2:", min_costo_2)


#cruce uniforme de los cromosomas seleccionados
def cruce_uniforme(cromosoma1, cromosoma2):
    hijo = []
    num_genes_intercambiar = np.random.randint(1, 3)
    genes_intercambiar = np.random.choice(len(cromosoma1), num_genes_intercambiar, replace=False)
    for i in range(len(cromosoma1)):
        if i in genes_intercambiar:
            hijo.append(cromosoma2[i])
        else:
            hijo.append(cromosoma1[i])
    return hijo


def leer_curso(file):
    cursos = []
    with open(file, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursos.append({'CLAVE': row['CLAVE'], '# GPOs': int(row['# GPOs'])})
    return cursos

# {'UF': ['TC1028', 8], 'Periodo': 'P1,P2', 'Profesor': 'Mauricio Paletta', 'Hora_inicio': ['11:00', '11:00', '19:00', '18:00', '12:00'], 'Hora_fin': ['13:00', '13:00', '21:00', '21:00', '16:00']}
def mutacion(cromosoma):
    cursos = leer_curso(file1)
    hijo = cromosoma[:]
    num_genes_mutar = 1
    genes_mutar = np.random.choice(len(cromosoma), num_genes_mutar, replace=False)
    
    # Verifica si genes_mutar está vacío
    if len(genes_mutar) == 0:
        print("Error: No se generaron genes para mutar")
        return hijo
    
    print("Genes a mutar:", [cromosoma[i] for i in genes_mutar])
    print("")
    #aleatoria eleige un atributo para mutar: Mutación de UF, Mutación de Periodo, Mutación de Profesor, Mutación Hora Inicio, Mutación Hora Fin
    atributo = np.random.randint(0, 5)
    if atributo == 0:
        print("============================ se mudo en UF ===========================")
        if hijo[genes_mutar[0]] in UF:
            #si grupo de la materia es 1 en array de cursos, se queda en 1
            for curso in cursos:
                if curso['CLAVE'] == hijo[genes_mutar[0]]["UF"][0]:
                    hijo[genes_mutar[0]]["UF"] = np.random.choice(UF) + ", " + str(np.random.randint(1, curso['# GPOs']))
                    print("se mutó en materia")
        else:
            #si es bloque, cambia el tema del bloque correspondiente
            #['TC2008B-3', 1]
            for bloque in bloques:
                if hijo[genes_mutar[0]]["UF"][0] in bloques[bloque]:
                    hijo[genes_mutar[0]]["UF"] = np.random.choice(bloques[bloque]) + ", " + str("1")
                    print("se mutó en bloque")
            
    elif atributo == 1:
        print("============================ se mudo en periodo ===========================")
        hijo[genes_mutar[0]]["Periodo"] = random.choice(periodos)
    elif atributo == 2:
        print("============================ se mudo en profesor ===========================")
        hijo[genes_mutar[0]]['Profesor'] = random.choice(lista_profesor_materia)
    elif atributo == 3:
        print("============================ se mudo en hora inicio ===========================")
        hora_inicio = [] 
        # de 7 a 19 horas
        for i in range(5):
            hora_random = np.random.randint(7, 19)
            hora_inicio.append(str(hora_random) + ":" + str("00"))
        hijo[genes_mutar[0]]["Hora_inicio"] = hora_inicio
    elif atributo == 4:
        print("============================ se mudo en hora fin ===========================")
        # hora_fin = hora inicio + 2 a 4 horas
        hora_fin = []
        for i in range(5):
            hora_random = np.random.randint(2, 4)
            hora_fin.append(str(int(hijo[genes_mutar[0]]["Hora_inicio"][i][0:2]) + hora_random) + ":" + str("00"))
        hijo[genes_mutar[0]]["Hora_fin"] = hora_fin
    return hijo

 
# min_costo_cromosoma_1 = [0, 0, 0, 0, 0]
# min_costo_cromosoma_2 = [1, 1, 1, 1, 1]
hijo = cruce_uniforme(min_costo_cromosoma_1, min_costo_cromosoma_2)

print("Padre 1:", min_costo_cromosoma_1)
print("")
print("Padre 2:", min_costo_cromosoma_2)
print("")
print("Hijo:", hijo)

# mutante = mutacion(min_costo_cromosoma_1)
# #print("Mutante:", mutante)
# for i in range(len(mutante)):
#     print(i, mutante[i])


#guardar los cromosomas seleccionados en una poblacion nueva
# new_poblacion1 = []
# new_poblacion1.append(min_costo_cromosoma_1)
# new_poblacion1.append(min_costo_cromosoma_2)

# print("Nueva población:")
# for i in range(len(new_poblacion1)):
#     print(new_poblacion1[i])


