import random
from funcoes_apoio import copiar_solucao, avalia_solucao, horas_trabalhadas
from subida_encosta import subida_encosta

def tentativa_perturbada(solucao_inicial, tempo, limite_horas):
    tentativa = copiar_solucao(solucao_inicial)
    tecnicos = list(tentativa.keys())

    escolha = random.choice(["move", "swap"])

    if escolha == "move":
        t_origem = random.choice(tecnicos)
        if tentativa[t_origem]:
            m = random.choice(tentativa[t_origem])
            candidatos = [t for t in tecnicos if t != t_origem and isinstance(tempo.get(t, {}).get(m), (int, float))]
            if candidatos:
                t_dest = random.choice(candidatos)
                tentativa[t_origem].remove(m)
                tentativa[t_dest].append(m)

    else:  
        t1, t2 = random.sample(tecnicos, 2)
        if tentativa[t1] and tentativa[t2]:
            m1 = random.choice(tentativa[t1])
            m2 = random.choice(tentativa[t2])

            if isinstance(tempo.get(t1, {}).get(m2), (int, float)) and isinstance(tempo.get(t2, {}).get(m1), (int, float)):
                tentativa[t1].remove(m1)
                tentativa[t2].remove(m2)
                tentativa[t1].append(m2)
                tentativa[t2].append(m1)

    horas = horas_trabalhadas(tentativa, tempo)
    for t in horas:
        if horas[t] > limite_horas.get(t, 8):
            return copiar_solucao(solucao_inicial)  

    return tentativa

def subida_encosta_tentativas(solucao_inicial, tempo, limite_horas, num_tentativas=10):

    custo_inicial = avalia_solucao(solucao_inicial, tempo)

    melhor_solucao = copiar_solucao(solucao_inicial)
    melhor_custo = custo_inicial

    for _ in range(max(1, int(num_tentativas))):
        start = tentativa_perturbada(solucao_inicial, tempo, limite_horas)
        sol_final, custo_final = subida_encosta(start, tempo, limite_horas)

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