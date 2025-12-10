import random
from copy import deepcopy

PENALTY = 10**6

def gerar_populacao_inicial(tam_pop, tecnicos, maquinas, turnos_tecnicos,
                            turnos_permitidos, tempo, limite_horas):
    populacao = []
    for _ in range(tam_pop):
        individuo = {t: [] for t in tecnicos}

        # embaralha máquinas para variar indivíduos
        m_shuffled = maquinas[:]
        random.shuffle(m_shuffled)

        for m in m_shuffled:
            
            elegiveis = [t for t in tecnicos if turnos_tecnicos.get(t) in turnos_permitidos.get(m, [])]
            if not elegiveis:
               
                elegiveis = tecnicos[:]
            escolha = random.choice(elegiveis)
            individuo[escolha].append(m)

        populacao.append(individuo)
    return populacao


def avalia_solucao(solucao, tempo, turnos_tecnicos, turnos_permitidos, limite_horas):
    custo_total = 0.0
    horas = {t: 0.0 for t in solucao}

    for t, maquinas in solucao.items():
        for m in maquinas:
            # verifica se técnico tem tempo declarado para a máquina
            val = tempo.get(t, {}).get(m)
            if val is None:
                # pode ser que exista tempo para outro técnico mas não para este
                custo_total += PENALTY
                continue

            # verifica turno permitido
            if turnos_tecnicos.get(t) not in turnos_permitidos.get(m, []):
                custo_total += PENALTY
                horas[t] += val
                continue

            
            custo_total += val
            horas[t] += val

    
    for t, h in horas.items():
        if h > limite_horas.get(t, float('inf')):
            custo_total += PENALTY * (h - limite_horas.get(t, 0))

    return custo_total, horas


def fitness(solucao, tempo, turnos_tecnicos, turnos_permitidos, limite_horas):
    custo, _ = avalia_solucao(solucao, tempo, turnos_tecnicos, turnos_permitidos, limite_horas)
    return custo


def selecao_roleta(populacao, tempo, turnos_tecnicos, turnos_permitidos, limite_horas):

    custos = [fitness(ind, tempo, turnos_tecnicos, turnos_permitidos, limite_horas) for ind in populacao]
    # transforma em aptidão: apt = 1/(1+custo)
    apt = [1.0 / (1.0 + c) for c in custos]
    soma = sum(apt)
    if soma == 0:
        return deepcopy(random.choice(populacao))
    pick = random.uniform(0, soma)
    atual = 0.0
    for ind, a in zip(populacao, apt):
        atual += a
        if atual >= pick:
            return deepcopy(ind)
    return deepcopy(populacao[-1])


def crossover_maquina(pai, mae, tecnicos, maquinas, taxa_cross):

    if random.random() > taxa_cross:
        return deepcopy(pai), deepcopy(mae)

    filho1 = {t: [] for t in tecnicos}
    filho2 = {t: [] for t in tecnicos}

    for m in maquinas:
        
        t_pai = next((t for t, lst in pai.items() if m in lst), None)
        t_mae = next((t for t, lst in mae.items() if m in lst), None)

     
        if random.random() < 0.5:
            origem = t_pai
        else:
            origem = t_mae
    
        if origem is None:
            origem = random.choice(tecnicos)
        filho1[origem].append(m)

        if random.random() < 0.5:
            origem2 = t_mae
        else:
            origem2 = t_pai
        if origem2 is None:
            origem2 = random.choice(tecnicos)
        filho2[origem2].append(m)

    return filho1, filho2


def mutacao_reatribuicao(individuo, tecnicos, maquinas, turnos_tecnicos, turnos_permitidos, taxa_mut):
  
    if random.random() > taxa_mut:
        return individuo

 
    all_m = [m for lst in individuo.values() for m in lst]
    if not all_m:
        return individuo

    m = random.choice(all_m)

    
    t_atual = next((t for t, lst in individuo.items() if m in lst), None)
    if t_atual:
        individuo[t_atual].remove(m)

    elegiveis = [t for t in tecnicos if turnos_tecnicos.get(t) in turnos_permitidos.get(m, [])]
    if not elegiveis:
        elegiveis = tecnicos[:]

    t_novo = random.choice(elegiveis)
    individuo[t_novo].append(m)

    # chance de trocar outra máquina entre técnicos
    if random.random() < 0.3:
        t1, t2 = random.sample(tecnicos, 2)
        if individuo[t1] and individuo[t2]:
            m1 = random.choice(individuo[t1])
            m2 = random.choice(individuo[t2])
            individuo[t1].remove(m1); individuo[t2].remove(m2)
            individuo[t1].append(m2); individuo[t2].append(m1)

    return individuo


def algoritmo_genetico(solucao_inicial, tempo, turnos_tecnicos, turnos_permitidos,limite_horas, tam_pop, num_geracoes, taxa_cross, taxa_mut,tecnicos=None, elitismo=0.1):

    if tecnicos is None:
        tecnicos = list(solucao_inicial.keys())

 
    maquinas = sorted(list(turnos_permitidos.keys()))

    populacao = gerar_populacao_inicial(tam_pop, tecnicos, maquinas, turnos_tecnicos,
                                        turnos_permitidos, tempo, limite_horas)

    melhor_global = None
    melhor_custo = float("inf")


    n_elite = max(1, int(elitismo * tam_pop))

    for g in range(num_geracoes):
        avaliacoes = [(ind, fitness(ind, tempo, turnos_tecnicos, turnos_permitidos, limite_horas)) for ind in populacao]
        avaliacoes.sort(key=lambda x: x[1])  # menor custo primeiro

        
        if avaliacoes[0][1] < melhor_custo:
            melhor_custo = avaliacoes[0][1]
            melhor_global = deepcopy(avaliacoes[0][0])

      
        novos = [deepcopy(avaliacoes[i][0]) for i in range(n_elite)]

  
        while len(novos) < tam_pop:
            pai = selecao_roleta(populacao, tempo, turnos_tecnicos, turnos_permitidos, limite_horas)
            mae = selecao_roleta(populacao, tempo, turnos_tecnicos, turnos_permitidos, limite_horas)

            filho1, filho2 = crossover_maquina(pai, mae, tecnicos, maquinas, taxa_cross)

            filho1 = mutacao_reatribuicao(filho1, tecnicos, maquinas, turnos_tecnicos, turnos_permitidos, taxa_mut)
            filho2 = mutacao_reatribuicao(filho2, tecnicos, maquinas, turnos_tecnicos, turnos_permitidos, taxa_mut)

            novos.append(filho1)
            if len(novos) < tam_pop:
                novos.append(filho2)

        populacao = novos

    melhor_custo_final, _ = None, None
    if melhor_global is not None:
        melhor_custo_final, _ = avalia_solucao(melhor_global, tempo, turnos_tecnicos, turnos_permitidos, limite_horas)
    else:

        melhor_global = deepcopy(populacao[0])
        melhor_custo_final, _ = avalia_solucao(melhor_global, tempo, turnos_tecnicos, turnos_permitidos, limite_horas)

    return melhor_global, melhor_custo_final
