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

    if temp_inicial is None or not isinstance(temp_inicial, (int, float)) or temp_inicial <= 0:
        temp_inicial = 100.0
    if temp_final is None or not isinstance(temp_final, (int, float)) or temp_final <= 0:
        temp_final = 0.1
    if fator_redutor is None or not isinstance(fator_redutor, (float, int)) or not (0 < fator_redutor < 1):
        fator_redutor = 0.95

    solucao_atual = copiar_solucao(solucao_inicial)
    custo_atual = avalia_solucao(solucao_atual, tempo)

    melhor_solucao = copiar_solucao(solucao_atual)
    melhor_custo = custo_atual

    temperatura = float(temp_inicial)
    iteracoes = 0
    max_iter = 20000  # safety cap

    while temperatura > temp_final and iteracoes < max_iter:
        vizinhos = gerar_vizinhos(solucao_atual, tempo, limite_horas)
        if not vizinhos:
            break

        vizinho = random.choice(vizinhos)
        custo_vizinho = avalia_solucao(vizinho, tempo)

        prob = probabilidade_aceitacao(custo_atual, custo_vizinho, temperatura)
        if random.random() < prob:
            solucao_atual = copiar_solucao(vizinho)
            custo_atual = custo_vizinho
            if custo_atual < melhor_custo:
                melhor_solucao = copiar_solucao(solucao_atual)
                melhor_custo = custo_atual

        temperatura *= fator_redutor
        iteracoes += 1

    return melhor_solucao, melhor_custo