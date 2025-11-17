# tempera_simulada.py
import random
import math
from funcoes_apoio import gerar_vizinhos, avalia_solucao, copiar_solucao

def probabilidade_aceitacao(custo_atual, custo_vizinho, temp):
    if custo_vizinho < custo_atual:
        return 1.0
    try:
        return math.exp(-(custo_vizinho - custo_atual) / temp)
    except OverflowError:
        return 0.0

def tempera_simulada(solucao_inicial, tempo, limite_horas, temp_inicial=None, temp_final=None, fator_redutor=None):

    solucao_atual = copiar_solucao(solucao_inicial)
    custo_atual = avalia_solucao(solucao_atual, tempo)

    melhor_solucao = copiar_solucao(solucao_atual)
    melhor_custo = custo_atual

    temperatura = float(temp_inicial)

    while temperatura > temp_final :

        vizinhos = gerar_vizinhos(solucao_atual, tempo, limite_horas)
        if not vizinhos:
            break

        vizinho = random.choice(vizinhos)
        custo_vizinho = avalia_solucao(vizinho, tempo)
        print("Custo atual:", custo_atual)
        for v in vizinhos[:5]:
            print(" → vizinho:", avalia_solucao(v, tempo)) 
        prob = probabilidade_aceitacao(custo_atual, custo_vizinho, temperatura)
        if random.random() < prob:
            solucao_atual = copiar_solucao(vizinho)
            custo_atual = custo_vizinho
            if custo_atual < melhor_custo:
                melhor_solucao = copiar_solucao(solucao_atual)
                melhor_custo = custo_atual

        temperatura *= fator_redutor

    return melhor_solucao, melhor_custo
