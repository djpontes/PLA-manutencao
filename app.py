from flask import Flask, render_template, request, jsonify
from funcoes import gerar_problema, gerar_solucao_inicial, avalia
from subida_encosta import subida_encosta, avalia_solucao
from subida_encosta_tentativa import subida_encosta_tentativas
from tempera_simulada import tempera_simulada
from analise_metodos import analisar_metodos
from algoritmo_genetico import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/executar_ag", methods=["POST"])
def executar_ag():
    data = request.get_json()
    print("=== RECEBIDO NO /executar_ag ===")
    print(data)

    solucao_inicial = data.get("solucao_inicial")
    tempo = data.get("tempo")
    turnos_tecnicos = data.get("turnos_tecnicos")
    turnos_permitidos = data.get("turnos_permitidos")
    limite_horas = data.get("limite_horas")

    # aceitar tanto 'tamanho_pop' quanto 'tam_pop' (frontend já usou 'tamanho_pop')
    tam_pop = int(data.get("tamanho_pop", data.get("tam_pop", 10)))
    num_geracoes = int(data.get("num_geracoes", 20))
    taxa_cross = float(data.get("taxa_cross", 0.8))
    taxa_mut = float(data.get("taxa_mut", 0.1))

    # validações básicas (evitam crashes)
    if solucao_inicial is None or tempo is None or turnos_tecnicos is None or turnos_permitidos is None:
        return jsonify({"erro": "Dados incompletos. Execute primeiro /metodos para gerar os dados."}), 400

    # executar o algoritmo genético
    melhor_solucao, melhor_custo = algoritmo_genetico(
        solucao_inicial,
        tempo,
        turnos_tecnicos,
        turnos_permitidos,
        limite_horas,
        tam_pop,
        num_geracoes,
        taxa_cross,
        taxa_mut
    )

    # calcular custo da solução inicial (usa 'avalia' importada de funcoes)
    try:
        custo_inicial = avalia(solucao_inicial, tempo)
    except Exception:
        # fallback se avalia tiver assinatura diferente
        custo_inicial = None

    # ganho absoluto e percentual (se possível)
    ganho_abs = None
    ganho_pct = None
    if custo_inicial is not None:
        ganho_abs = custo_inicial - melhor_custo
        if custo_inicial != 0:
            ganho_pct = (100.0 * ganho_abs) / custo_inicial

    return jsonify({
        "solucao_inicial": solucao_inicial,
        "custo_inicial": custo_inicial,
        "solucao_final": melhor_solucao,
        "custo_final": melhor_custo,
        "ganho_abs": ganho_abs,
        "ganho_pct": ganho_pct
    })




@app.route("/analise", methods=["POST"])
def analise():
    dados = request.json

    solucao_inicial = dados["solucao_inicial"]
    tempo = dados["tempo"]
    limite_horas = dados["limite_horas"]

    num_tentativas = dados.get("num_tentativas", 10)
    temp_ini = dados.get("temp_ini", 50)
    temp_fim = dados.get("temp_fim", 1)
    fator = dados.get("fator", 0.95)

    resultados = analisar_metodos(solucao_inicial, tempo, limite_horas,
                                  num_tentativas, temp_ini, temp_fim, fator)

    return jsonify({"resultados": resultados})

# ROTA PARA GERAR DADOS E SOLUÇÃO INICIAL
@app.route("/metodos", methods=["GET", "POST"])
def metodos():
    if request.method == "POST":
        data = request.get_json()
        tipo = data.get("tipo")
        tamanho = int(data.get("tamanho") or 5)

        # 1. Gerar problema
        tec, turnos_tecnicos, tempo, turnos_permitidos, limite_horas = gerar_problema(tipo, tamanho)

        # 2. Gerar solução inicial
        solucao, horas_trabalhadas = gerar_solucao_inicial(
            tec, turnos_tecnicos, tempo, turnos_permitidos, limite_horas
        )

        # 3. Avaliar solução
        custo = avalia(solucao, tempo)

        # 4. Máquinas não atribuídas
        maquinas_nao_atribuidas = [
            m for m in turnos_permitidos.keys()
            if all(m not in maquinas for maquinas in solucao.values())
        ]

        resultado_execucao = {
            "Técnicos": tec,
            "Turnos dos técnicos": turnos_tecnicos,
            "Tempo para manutenção": tempo,
            "Turnos permitidos": turnos_permitidos,
            "Limite de horas": limite_horas,
            "Solução inicial": solucao,
            "Horas trabalhadas": horas_trabalhadas,
            "Custo da solução inicial": custo,
            "Máquinas não atribuídas": maquinas_nao_atribuidas
        }
       

        return jsonify({"resultado_execucao": resultado_execucao})

    return render_template("metodos.html")


@app.route("/executar_metodo", methods=["POST"])
def executar_metodo():
    data = request.get_json()

    metodo = data.get("metodo")
    solucao_inicial = data["solucao_inicial"]
    tempo = data["tempo"]
    limite_horas = data["limite_horas"]

    # SUBIDA DE ENCOSTA NORMAL
    if metodo == "subida":
        custo_inicial = data.get("custo_inicial")
        try:
            custo_inicial = float(custo_inicial) if custo_inicial is not None else None
        except Exception:
            custo_inicial = None

        solucao_final, custo_final = subida_encosta(solucao_inicial, tempo, limite_horas)

        if custo_inicial is None:
            custo_inicial = avalia_solucao(solucao_inicial, tempo)

        if custo_inicial is not None and custo_inicial != 0:
            ganho = (100.0 * abs(custo_inicial - custo_final)) / custo_inicial
        else:
            ganho = None


        return jsonify({
            "solucao_inicial": solucao_inicial,
            "solucao_final": solucao_final,
            "custo_inicial": custo_inicial,
            "custo_final": custo_final,
            "ganho": ganho
        })


    # SUBIDA DE ENCOSTA COM TENTATIVAS
    elif metodo == "subida-tentativas":
        num_tentativas = int(data.get("num_tentativas", 10))

        resultado = subida_encosta_tentativas(
            solucao_inicial,
            tempo,
            limite_horas,
            num_tentativas
        )

        return jsonify(resultado)

    # TÊMPERA SIMULADA
    elif metodo == "tempera":
        temp_inicial = float(data.get("temp_inicial"))
        temp_final = float(data.get("temp_final"))
        fator_redutor = float(data.get("fator_redutor"))

        solucao_final, custo_final = tempera_simulada(
            solucao_inicial,
            tempo,
            limite_horas,
            temp_inicial,
            temp_final,
            fator_redutor
        )

        return jsonify({
            "solucao_final": solucao_final,
            "custo_final": custo_final
        })

    # MÉTODO INVÁLIDO
    return jsonify({"erro": "Método inválido"}), 400

if __name__ == "__main__":
    app.run(debug=True)