import random
from RL import verificar_horarios_continuos
from RD import verificar_solapamientos_cromosoma, verificar_horas
from generar_genes import generar_cromosomas

def funcion_costos(p_leves, p_duras):
    sumatoria_leves = sum(random.uniform(0.5, 1.5) for _ in range(p_leves))
    sumatoria_duras = sum(random.uniform(9.1, 10.1) for _ in range(p_duras))
    resultado = sumatoria_leves + sumatoria_duras
    return resultado

# obtener p_leves y p_duras de un cromosoma
def costo_cromosoma(cromosoma):
    p_leves = verificar_horarios_continuos(cromosoma) + verificar_solapamientos_cromosoma(cromosoma)
    p_duras = verificar_horas(cromosoma)
    return funcion_costos(p_leves, p_duras)

# # Genera la población
# file1 = "Agosto-Diciembre.csv"
# poblacion1 = [generar_cromosomas(file1) for _ in range(100)]

# # Evaluar la población
# costo = [costo_cromosoma(cromosoma) for cromosoma in poblacion1]
# print("Costos de la población:")
# for i in range(len(costo)):
#     print(i, costo[i])
