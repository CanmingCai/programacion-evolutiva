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
horario_clases = generar_horario_clases(profesor)
print(horario_clases)
