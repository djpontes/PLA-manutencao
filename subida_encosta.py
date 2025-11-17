from funcoes_apoio import copiar_solucao, horas_trabalhadas, gerar_vizinhos, avalia_solucao

def subida_encosta(solucao_inicial, tempo, limite_horas):
    atual = copiar_solucao(solucao_inicial)
    custo_atual = avalia_solucao(atual, tempo)

    while True:
        melhor_vizinho = None
        melhor_custo = float("inf")

        vizinhos = gerar_vizinhos(atual, tempo, limite_horas)
        if not vizinhos:
            break

        for v in vizinhos:
            c = avalia_solucao(v, tempo)
            if c < melhor_custo:
                melhor_custo = c
                melhor_vizinho = v

        if melhor_vizinho is None or melhor_custo >= custo_atual:
            break

        print("Custo atual:", custo_atual)
        for v in vizinhos[:5]:
            print(" → vizinho:", avalia_solucao(v, tempo)) 
        atual = melhor_vizinho
        custo_atual = melhor_custo
        

    return atual, custo_atual