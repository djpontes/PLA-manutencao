from copy import deepcopy

def copiar_solucao(solucao):
    return {t: list(ms) for t, ms in solucao.items()}

def horas_trabalhadas(solucao, tempo):
    horas = {t: 0 for t in solucao.keys()}
    for t, maquinas in solucao.items():
        for m in maquinas:
            val = tempo.get(t, {}).get(m)
            if isinstance(val, (int, float)):
                horas[t] += val
    return horas

def gerar_vizinhos(solucao, tempo, limite_horas):
    vizinhos = []
    tecnicos = list(solucao.keys())

    for i, t_origem in enumerate(tecnicos):
        for m in list(solucao[t_origem]):  
            for t_dest in tecnicos:
                if t_dest == t_origem:
                    continue

                val_dest = tempo.get(t_dest, {}).get(m)
                if not isinstance(val_dest, (int, float)):
                    continue

                nova = copiar_solucao(solucao)
                nova[t_origem] = list(nova[t_origem]) 
                nova[t_dest] = list(nova[t_dest])
                nova[t_origem].remove(m)
                nova[t_dest].append(m)

                horas = horas_trabalhadas(nova, tempo)
                if horas[t_dest] <= limite_horas.get(t_dest, 8) and horas[t_origem] <= limite_horas.get(t_origem, 8):
                    vizinhos.append(nova)

            for j in range(i+1, len(tecnicos)):
                t2 = tecnicos[j]
                for m2 in list(solucao[t2]):
                    v1 = tempo.get(t2, {}).get(m)
                    v2 = tempo.get(t_origem, {}).get(m2)
                    if not (isinstance(v1, (int, float)) and isinstance(v2, (int, float))):
                        continue

                    nova = copiar_solucao(solucao)
                    nova[t_origem] = list(nova[t_origem])
                    nova[t2] = list(nova[t2])

                    nova[t_origem].remove(m)
                    nova[t2].remove(m2)
                    nova[t_origem].append(m2)
                    nova[t2].append(m)

                    horas = horas_trabalhadas(nova, tempo)
                    if horas[t_origem] <= limite_horas.get(t_origem, 8) and horas[t2] <= limite_horas.get(t2, 8):
                        vizinhos.append(nova)
    # Remover duplicatas
    unique = []
    seen = set()
    for v in vizinhos:
        key = tuple(sorted((t, tuple(sorted(ms))) for t, ms in v.items()))
        if key not in seen:
            seen.add(key)
            unique.append(v)

    return unique

def avalia_solucao(solucao, tempo):
    custo = 0
    for t, maquinas in solucao.items():
        for m in maquinas:
            val = tempo.get(t, {}).get(m)
            if isinstance(val, (int, float)):
                custo += val
            else:
                # penalidade alta 
                custo += 1e6
    return custo
