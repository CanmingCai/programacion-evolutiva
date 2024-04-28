import csv
import random

def leer_periodos():
    periodos = {}
    with open('UDF.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            periodos[row['Clave']] = [row['P1'], row['P2'], row['P3']]
    return periodos

def generar_cromosomas():
    cromosoma = []

    periodos = leer_periodos()

    # 读取CSV文件并获取课程及其班级信息
    cursos = []
    with open('Febrero-Junio.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursos.append({'CLAVE': row['CLAVE'], '# GPOs': int(row['# GPOs'])})

    # 遍历课程，生成对应数量的班级
    for curso in cursos:
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
            cromosoma.append({'Uf': [curso['CLAVE'], grupo], 'Periodo': periodo})

    # 随机打乱课程及其班级的顺序
    random.shuffle(cromosoma)

    return cromosoma

# 生成100个包含10个随机课程及其班级的种群
# poblacion1 = [generar_cromosomas() for _ in range(100)]

# 打印生成的种群
# for i, cromosoma in enumerate(poblacion1, 1):
#     print(f"Cromosoma {i}:")
#     for curso in cromosoma:
#         print(curso)
#     print()

print(generar_cromosomas())