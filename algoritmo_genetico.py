import random
from copy import deepcopy
from funcoes import avalia

# ---------------------------------------------------------
# GERA POPULAÇÃO INICIAL
# ---------------------------------------------------------
def gerar_populacao_inicial(n, solucao_inicial):
    populacao = []
    for _ in range(n):
        novo = deepcopy(solucao_inicial)

        # Embaralha máquinas entre os técnicos
        maquinas = []
        for mlist in novo.values():
            maquinas.extend(mlist)

        random.shuffle(maquinas)

        # Redistribui
        i = 0
        for t in novo.keys():
            qtd = len(novo[t])
            novo[t] = maquinas[i:i+qtd]
            i += qtd

        populacao.append(novo)
    return populacao


# ---------------------------------------------------------
# AVALIA aptidão (fitness)
# ---------------------------------------------------------
def fitness(solucao, tempo, *args, **kwargs):
    return avalia(solucao, tempo)



# ---------------------------------------------------------
# SELEÇÃO (roleta)
# ---------------------------------------------------------
def selecao(populacao, tempo, turnos_tecnicos, turnos_permitidos, limite_horas):
    custos = [fitness(ind, tempo, turnos_tecnicos, turnos_permitidos, limite_horas) for ind in populacao]
    total = sum(1/(c+1) for c in custos)

    pick = random.uniform(0, total)
    atual = 0

    for ind, c in zip(populacao, custos):
        atual += 1/(c+1)
        if atual >= pick:
            return deepcopy(ind)

    return deepcopy(populacao[-1])

# ---------------------------------------------------------
# CROSSOVER
# ---------------------------------------------------------
def crossover(pai, mae, taxa):
    if random.random() > taxa:
        return deepcopy(pai), deepcopy(mae)

    filho1 = deepcopy(pai)
    filho2 = deepcopy(mae)

    tecnicos = list(pai.keys())
    corte = random.randint(1, len(tecnicos)-1)

    for t in tecnicos[:corte]:
        filho1[t], filho2[t] = filho2[t], filho1[t]

    return filho1, filho2


# ---------------------------------------------------------
# MUTAÇÃO
# ---------------------------------------------------------
def mutacao(individuo, taxa):
    if random.random() > taxa:
        return individuo

    tecnicos = list(individuo.keys())

    t1, t2 = random.sample(tecnicos, 2)

    if len(individuo[t1]) == 0:
        return individuo

    m = random.choice(individuo[t1])
    individuo[t1].remove(m)
    individuo[t2].append(m)

    return individuo


# ---------------------------------------------------------
# ALGORITMO GENÉTICO PRINCIPAL
# ---------------------------------------------------------
def algoritmo_genetico(solucao_inicial, tempo, turnos_tecnicos, turnos_permitidos, limite_horas, tam_pop, num_geracoes, taxa_cross, taxa_mut):
    populacao = gerar_populacao_inicial(tam_pop, solucao_inicial)

    melhor_global = None
    melhor_custo = float("inf")

    for g in range(num_geracoes):
        nova_populacao = []

        while len(nova_populacao) < tam_pop:
            pai = selecao(populacao, tempo, turnos_tecnicos, turnos_permitidos, limite_horas)
            mae = selecao(populacao, tempo, turnos_tecnicos, turnos_permitidos, limite_horas)

            filho1, filho2 = crossover(pai, mae, taxa_cross)

            filho1 = mutacao(filho1, taxa_mut)
            filho2 = mutacao(filho2, taxa_mut)

            nova_populacao.append(filho1)
            if len(nova_populacao) < tam_pop:
                nova_populacao.append(filho2)

        populacao = nova_populacao

        # Melhor da geração
        for ind in populacao:
            c = fitness(ind, tempo, turnos_tecnicos, turnos_permitidos, limite_horas)
            if c < melhor_custo:
                melhor_custo = c
                melhor_global = deepcopy(ind)

    return melhor_global, melhor_custo