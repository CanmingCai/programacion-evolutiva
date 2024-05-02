import random
from datetime import time

# Diccionario de horarios de profesores
horario_profesor = {
    "Jose Aguilera": {
        "Lunes": [time(9, 0), time(13, 0), time(17, 0), time(20, 0)],
        "Martes": [time(0, 0), time(0, 0)],
        "Miercoles": [time(9, 0), time(13, 0), time(17, 0), time(20, 0)],
        "Jueves": [time(0, 0), time(0, 0)],
        "Viernes": [time(9, 0), time(13, 0), time(17, 0), time(20, 0)]
    }
}

def generar_horario_clases(profesor):
    horario_clases = {
        "Hora_inicio": [],
        "Hora_fin": []
    }
    for dia in ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]:
        horario_disponible = horario_profesor[profesor][dia]
        if horario_disponible[0] != time(0, 0):
            # Seleccionar aleatoriamente un horario de inicio
            hora_inicio = random.choice(horario_disponible[::2])  # Cada segundo elemento es una hora de inicio
            indice_inicio = horario_disponible.index(hora_inicio)
            # Calcular el horario de finalización
            hora_fin = hora_inicio.replace(hour=hora_inicio.hour + random.randint(2, 4))
            # Asegurarse de que el horario de finalización no exceda el horario de salida
            if hora_fin > horario_disponible[indice_inicio + 1]:
                hora_fin = horario_disponible[indice_inicio + 1]
            horario_clases["Hora_inicio"].append(hora_inicio.strftime("%H:%M"))
            horario_clases["Hora_fin"].append(hora_fin.strftime("%H:%M"))
        else:
            horario_clases["Hora_inicio"].append("NA")
            horario_clases["Hora_fin"].append("NA")
    return horario_clases

# Ejemplo de uso para el profesor Jose Aguilera
profesor = "Jose Aguilera"
#horario_clases = generar_horario_clases(profesor)
#print(horario_clases)


#--------------- cruces uniformes
import random

def cruce_uniforme(padre1, padre2):
    hijo = padre1[:]  # Creamos una copia del padre1 para inicializar al hijo
    for i in range(len(padre1)):
        # Determinamos si se intercambia el gen en esta posición
        if random.random() < 0.5:
            hijo[i] = padre2[i]
    return hijo

# Ejemplo de uso
padre1 = [1, 7, 3, 4, 5]
padre2 = [6, 2, 8, 9, 10]
hijo = cruce_uniforme(padre1, padre2)
print("Padre 1:", padre1)
print("Padre 2:", padre2)
print("Hijo:", hijo)


