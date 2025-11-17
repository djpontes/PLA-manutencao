import random

# Dados Fixos
tecnicos = ["T1", "T2", "T3", "T4", "T5", "T6"]
turnos_tecnicos = {"T1": "manhã", "T2": "manhã", "T3": "tarde", "T4": "tarde", "T5": "noite", "T6": "noite"}
limite_horas = {t: 8 for t in tecnicos} 

tempo = {
    "T1": {"M01": 3, "M02": 2, "M03": 4, "M10": 2},
    "T2": {"M01": 4, "M02": 3, "M03": 3, "M10": 3},
    "T3": {"M03": 3, "M04": 3, "M05": 2, "M06": 3, "M09": 3},
    "T4": {"M03": 2, "M04": 4, "M05": 3, "M06": 3, "M09": 3},
    "T5": {"M06": 5, "M07": 4, "M08": 3, "M09": 2, "M10": 3},
    "T6": {"M06": 4, "M07": 3, "M08": 2, "M09": 3, "M10": 2}
}

turnos_permitidos = {
    "M01": ["manhã"], "M02": ["manhã"], "M03": ["manhã", "tarde"],
    "M04": ["tarde"], "M05": ["tarde"], "M06": ["tarde", "noite"],
    "M07": ["noite"], "M08": ["noite"], "M09": ["tarde", "noite"],
    "M10": ["manhã", "noite"]
}


def ajustar_tempo_por_turno(tecnicos, turnos_tecnicos, tempo, turnos_permitidos):
    tempo_ajustado = {}
    for t in tecnicos:
        tempo_ajustado[t] = {}
        for m in tempo[t]:
            if turnos_tecnicos[t] in turnos_permitidos[m]:
                tempo_ajustado[t][m] = tempo[t][m]
            else:
                tempo_ajustado[t][m] = "-"  
    return tempo_ajustado

def gerar_problema(tipo="fixo", num_maquinas=5):
    if tipo == "fixo":
        return tecnicos, turnos_tecnicos, tempo, turnos_permitidos, limite_horas

    else:
        # mantem a quantidade de técnicos fixa
        tec = tecnicos
        turnos = ["manhã", "tarde", "noite"]

        # Gera máquinas aleatórias
        maquinas = [f"M{i+1:02}" for i in range(num_maquinas)]

        turnos_tecnicos_random = {t: random.choice(turnos) for t in tec}
        tempo_random = {t: {m: random.randint(1, 5) for m in maquinas} for t in tec}
        turnos_permitidos_random = {m: random.sample(turnos, k=random.randint(1, 3)) for m in maquinas}

        tempo_final = ajustar_tempo_por_turno(tec, turnos_tecnicos_random, tempo_random, turnos_permitidos_random)

        return tec, turnos_tecnicos_random, tempo_final, turnos_permitidos_random, limite_horas


# Atribui tarefas aos técnicos respeitando os turnos e limites de horas    
def gerar_solucao_inicial(tecnicos, turnos_tecnicos, tempo, turnos_permitidos, limite_horas):
    solucao = {t: [] for t in tecnicos}
    horas_trabalhadas = {t: 0 for t in tecnicos}

    for m in turnos_permitidos.keys():
        melhor_tecnico = None
        melhor_tempo = float('inf')

        for t in tecnicos:
            if m in tempo.get(t, {}) and turnos_tecnicos[t] in turnos_permitidos[m]:
                horas = tempo[t][m]
                if horas_trabalhadas[t] + horas <= limite_horas[t]:
                    if horas < melhor_tempo:
                        melhor_tempo = horas
                        melhor_tecnico = t

        if melhor_tecnico:
            solucao[melhor_tecnico].append(m)
            horas_trabalhadas[melhor_tecnico] += melhor_tempo
        else:
            print(f"Nenhum técnico disponível para a máquina {m}")
    
    print("SOLUCAO INICIAL:", solucao)

    return solucao, horas_trabalhadas

def avalia(solucao, tempo):
    custo_total = 0
    for t, maquinas in solucao.items():
        for m in maquinas:
            custo_total += tempo[t][m]
    return custo_total