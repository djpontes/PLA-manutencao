# subida_encosta_tentativas.py
import random
from funcoes_apoio import copiar_solucao, avalia_solucao
from subida_encosta import subida_encosta

def subida_encosta_tentativas(solucao_inicial, tempo, limite_horas, num_tentativas):
    custo_inicial = avalia_solucao(solucao_inicial, tempo)

    melhor_solucao = copiar_solucao(solucao_inicial)
    melhor_custo = custo_inicial

    for _ in range(num_tentativas):
        sol_final, custo_final = subida_encosta(
            solucao_inicial, 
            tempo,
            limite_horas
        )

        if custo_final < melhor_custo:
            melhor_custo = custo_final
            melhor_solucao = sol_final

    ganho = custo_inicial - melhor_custo

    return {
        "solucao_inicial": solucao_inicial,
        "solucao_final": melhor_solucao,
        "custo_inicial": custo_inicial,
        "custo_final": melhor_custo,
        "ganho": ganho
    }
