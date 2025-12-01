import time
from funcoes_apoio import avalia_solucao
from subida_encosta import subida_encosta
from subida_encosta_tentativa import subida_encosta_tentativas
from tempera_simulada import tempera_simulada

def calcular_ganho(custo_inicial, custo_final):
    if custo_inicial == 0:
        return 0
    return round(100 * abs(custo_inicial - custo_final) / custo_inicial, 2)

def analisar_metodos(solucao_inicial, tempo, limite_horas,
                     num_tentativas=10, temp_ini=50, temp_fim=1, fator=0.95):

    resultados = []
    custo_inicial = avalia_solucao(solucao_inicial, tempo)

    # 1. Subida simples
    t0 = time.time()
    sol_final1, custo1 = subida_encosta(solucao_inicial, tempo, limite_horas)
    t1 = time.time()
    resultados.append({
        "Método": "Subida de Encosta",
        "Solução Inicial": custo_inicial,
        "Solução Final": custo1,
        "Ganho (%)": calcular_ganho(custo_inicial, custo1),
        "Tempo Execução": round(t1 - t0, 4)
    })

    # 2. Subida por tentativas
    t0 = time.time()
    r2 = subida_encosta_tentativas(solucao_inicial, tempo, limite_horas, num_tentativas)
    t1 = time.time()
    custo2 = r2["custo_final"]
    resultados.append({
        "Método": "Subida por Tentativas",
        "Solução Inicial": custo_inicial,
        "Solução Final": custo2,
        "Ganho (%)": calcular_ganho(custo_inicial, custo2),
        "Tempo Execução": round(t1 - t0, 4)
    })

    # 3. Têmpera Simulada
    t0 = time.time()
    sol_final3, custo3 = tempera_simulada(solucao_inicial, tempo, limite_horas,
                                          temp_ini, temp_fim, fator)
    t1 = time.time()
    resultados.append({
        "Método": "Têmpera Simulada",
        "Solução Inicial": custo_inicial,
        "Solução Final": custo3,
        "Ganho (%)": calcular_ganho(custo_inicial, custo3),
        "Tempo Execução": round(t1 - t0, 4)
    })

    return resultados