import random
from RL import verificar_horarios_continuos, revisar_horarios_semestres, revisar_miercoles, verificar_duraciones
from RD import verificar_solapamientos_cromosoma, verificar_horas, revisar_horarios_colision, revisar_horas_excedidas, revisar_disponibilidad_profesores, verificar_franja_horarios, validar_horario
from generar_genes import generar_cromosomas, horario_profesor

def funcion_costos(p_leves, p_duras):
    sumatoria_leves = sum(random.uniform(0.5, 1.5) for _ in range(p_leves))
    sumatoria_duras = sum(random.uniform(9.1, 10.1) for _ in range(p_duras))
    resultado = sumatoria_leves + sumatoria_duras
    return resultado

# obtener p_leves y p_duras de un cromosoma
def costo_cromosoma(cromosoma):
    p_leves = verificar_horarios_continuos(cromosoma) + revisar_horarios_semestres(cromosoma, "UDF.csv") + revisar_miercoles(cromosoma) + verificar_duraciones(cromosoma)
    p_duras = verificar_horas(cromosoma) + verificar_solapamientos_cromosoma(cromosoma) + revisar_horarios_colision(cromosoma)  + revisar_horas_excedidas(cromosoma, "UDF.csv") + revisar_disponibilidad_profesores(cromosoma) + verificar_franja_horarios(horario_profesor,cromosoma) + validar_horario(cromosoma)
    return funcion_costos(p_leves, p_duras)

# # Genera la población
# file1 = "Agosto-Diciembre.csv"
# poblacion1 = [generar_cromosomas(file1) for _ in range(100)]

# # Evaluar la población
# costo = [costo_cromosoma(cromosoma) for cromosoma in poblacion1]
# print("Costos de la población:")
# for i in range(len(costo)):
#     print(i, costo[i])
