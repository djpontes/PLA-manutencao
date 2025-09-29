from flask import Flask, render_template, request, jsonify
from funcoes import gerar_problema, gerar_solucao_inicial, avalia

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

from flask import Flask, render_template, request, jsonify
from funcoes import gerar_problema, gerar_solucao_inicial, avalia

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/metodos", methods=["GET", "POST"])
def metodos():
    if request.method == "POST":
        data = request.get_json()
        tipo = data.get("tipo")
        tamanho = int(data.get("tamanho") or 5)

        # 1. Gerar problema
        tec, turnos_tecnicos, tempo, turnos_permitidos, limite_horas = gerar_problema(tipo, tamanho)

        # 2. Gerar solução inicial
        solucao, horas_trabalhadas = gerar_solucao_inicial(tec, turnos_tecnicos, tempo, turnos_permitidos, limite_horas)

        # 3. Avaliar solução
        custo = avalia(solucao, tempo)

        # 4. Lista de máquinas não atribuídas
        maquinas_nao_atribuidas = [m for m in turnos_permitidos.keys() if all(m not in maquinas for maquinas in solucao.values())]

        # 5. Monta o resultado como dicionário (para tabela)
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

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/algoritmos")
def algoritmos():
    return render_template("algoritmos.html")

if __name__ == "__main__":
    app.run(debug=True)
