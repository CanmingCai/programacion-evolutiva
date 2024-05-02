import numpy as np
from generar_genes import generar_cromosomas

lista_profesor_materia = ['Victor Manion', 'Juan Alvarado', 'Roberto Leyva', 'Mauricio Paletta', 'Yerly Flores', 'Jaime Lopez', 'Jorge Rodriguez', 'Jose Aguilera', 'Luis Guadarrama', 'Pedro Hernandez', 'Maria Mirafuentes', 'Roberto Vera', 'Octavio Silva', 'Fernando Ruiz', 'Ivan Olmos', 'Israel Tabarez']
periodos = [["P1,P2,P3"], ["P1,P2"], ["P2,P3"], ["P1"], ["P2"], ["P3"]]
UF =  ["TC1027", "TC1028", "TC1029", "TC1030", "TC1031", "TC1032", "TC1033", "TC2037", "TC2038", "TI1015"]


# Genera los costos aleatorios
costo = np.random.uniform(5, 40, 100)
# Imprime el índice de la lista de costos
for i in range(len(costo)):
    print(i, costo[i])

# from evaluar_costo import costo_evaluar
# costo_cromosomas = [costo_evaluar(cromosoma) for cromosoma in poblacion]
# print("Costos de los cromosomas:")


def torneo_seleccion(poblacion, costo, cantidad=25):
    # Selecciona n cromosomas aleatorios
    selec_indices = np.random.choice(len(poblacion), cantidad, replace=False)
    selec_cromosomas = [poblacion[i] for i in selec_indices]
    
    # Encuentra el cromosoma con el costo mínimo entre los seleccionados
    min_costo_index = min(selec_indices, key=lambda x: costo[x])
    min_costo_cromosoma = poblacion[min_costo_index]
    min_costo = costo[min_costo_index]
    
    return selec_cromosomas, min_costo_cromosoma, min_costo

# Genera la población
file1 = "Agosto-Diciembre.csv"
poblacion1 = [generar_cromosomas(file1) for _ in range(100)]

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

# {'UF': ['TC1028', 8], 'Periodo': 'P1,P2', 'Profesor': 'Mauricio Paletta', 'Hora_inicio': ['11:00', '11:00', '19:00', '18:00', '12:00'], 'Hora_fin': ['13:00', '13:00', '21:00', '21:00', '16:00']}
def mutacion(cromosoma):
    hijo = cromosoma[:]
    num_genes_mutar = 1
    genes_mutar = np.random.choice(len(cromosoma), num_genes_mutar, replace=False)
    #随机在Mutación de UF, Mutación de Periodo, Mutación de Profesor, Mutación Hora Inicio, Mutación Hora Fin选择一个进行变异
    atributo = np.random.randint(0, 5)
    if atributo == 0:
        if hijo[genes_mutar[0]] in UF:
            hijo[genes_mutar[0]] = np.random.choice(UF) + " " + str(np.random.randint(1, 8))
        else:
            hijo[genes_mutar[0]] = np.random.choice(UF) + " " + str(np.random.randint(1, 8))
    elif atributo == 1:
        hijo[genes_mutar[1]] = np.random.choice(periodos)
    elif atributo == 2:
        hijo[genes_mutar[2]] = np.random.choice(lista_profesor_materia)
    elif atributo == 3:
        hora_inicio = [] 
        # de 7 a 19 horas
        for i in range(5):
            hora_random = np.random.randint(7, 19)
            hora_inicio.append(str(hora_random) + ":" + str("00"))
        hijo[genes_mutar[3]] = hora_inicio
    elif atributo == 4:
        # hora inicio + 2 a 4 horas
        hora_fin = np.random.randint(7, 18)
        min_fin = np.random.choice([0, 30])
        hijo[genes_mutar[0]] = str(hora_fin) + ":" + str(min_fin)
 
min_costo_cromosoma_1 = [1, 7, 3, 4, 5]
min_costo_cromosoma_2 = [6, 2, 8, 9, 10]
hijo = cruce_uniforme(min_costo_cromosoma_1, min_costo_cromosoma_2)


print("Padre 1:", min_costo_cromosoma_1)
print("")
print("Padre 2:", min_costo_cromosoma_2)
print("")
print("Hijo:", hijo)

#guardar los cromosomas seleccionados en una poblacion nueva
# new_poblacion1 = []
# new_poblacion1.append(min_costo_cromosoma_1)
# new_poblacion1.append(min_costo_cromosoma_2)

# print("Nueva población:")
# for i in range(len(new_poblacion1)):
#     print(new_poblacion1[i])


