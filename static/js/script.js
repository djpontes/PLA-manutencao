window.ultimoResultadoExecucao = null;

// Função para alternar entre os conteúdos
function showContent(id) {
    let contents = document.querySelectorAll(".content");
    contents.forEach(c => c.classList.add("hidden"));

    let selected = document.getElementById(id);
    if (selected) {
        selected.classList.remove("hidden");
    }

    document.querySelectorAll(".menu-btn").forEach(btn => {
        btn.classList.remove("active");
    });

    const clickedBtn = document.querySelector(`.menu-btn[onclick="showContent('${id}')"]`);
    if (clickedBtn) {
        clickedBtn.classList.add("active");
    }

    if (window.innerWidth < 768) {
        window.scrollTo({
            top: document.getElementById(id).offsetTop - 20,
            behavior: 'smooth'
        });
    }
}


async function executarMetodo() {
    const metodo = document.getElementById("metodo").value;
    if (!metodo) {
        alert("Por favor, escolha um método válido!");
        return;
    }

    const resultadoDiv = document.getElementById("resultado-metodo");
    resultadoDiv.classList.remove("hidden");
    resultadoDiv.innerHTML = "<h3>Processando método...</h3>";

    const r = window.ultimoResultadoExecucao;
    if (!r) {
        alert("Primeiro gere a solução inicial.");
        resultadoDiv.classList.add("hidden");
        return;
    }

    try {
        let payload = {
            metodo: metodo,
            solucao_inicial: r["Solução inicial"],
            tempo: r["Tempo para manutenção"],
            limite_horas: r["Limite de horas"],
            custo_inicial: r["Custo da solução inicial"]
        };

        // --------------------------
        // SUBIDA COM TENTATIVAS
        // --------------------------
        if (metodo === "subida-tentativas") {
            payload["num_tentativas"] = parseInt(document.getElementById("num-tentativas").value);
        }

        // --------------------------
        // TÊMPERA SIMULADA
        // --------------------------
        if (metodo === "tempera") {
            payload["temp_inicial"] = parseFloat(document.getElementById("temp-inicial").value);
            payload["temp_final"] = parseFloat(document.getElementById("temp-final").value);
            payload["fator_redutor"] = parseFloat(document.getElementById("fator-redutor").value);
        }


        const resp = await fetch("/executar_metodo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await resp.json();


        const custoInicial = Number(r["Custo da solução inicial"]);
        const custoFinal = Number(data.custo_final);

        const ganho = custoInicial === 0
            ? "N/A"
            : ((100 * Math.abs(custoInicial - custoFinal)) / custoInicial).toFixed(2) + " %";

        const nomeMetodo = metodo === "tempera"
            ? "Têmpera Simulada"
            : metodo === "subida" 
                ? "Subida de Encosta"
                : "Subida de Encosta com Tentativas";

        resultadoDiv.innerHTML = `
            <h3>Resultado do método: ${nomeMetodo}</h3>

            <h4>Solução inicial (custo = ${custoInicial}):</h4>
            ${montarTabela(r["Solução inicial"])}

            <h4>Solução final (custo = ${custoFinal}):</h4>
            ${montarTabela(data.solucao_final)}

            <p><strong>Ganho:</strong> ${ganho}</p>
        `;
    } catch (err) {
        console.error(err);
        resultadoDiv.innerHTML = "<p>Por favor, preencha todos os campos</p>";
    }
}

function montarTabela(solucao) { 
    let html = `
        <table border="1" cellpadding="6" style="border-collapse: collapse; margin-bottom: 20px;">
            <tr style="background:#eee;">
                <th>Técnico</th>
                <th>Máquinas</th>
            </tr>
    `;

    for (const tecnico in solucao) { 
        const maquinas = solucao[tecnico]; 
        
        html += `
            <tr>
                <td><strong>${tecnico}</strong></td>
                <td>${maquinas.length > 0 ? maquinas.join(", ") : ""}</td>
            </tr>
        `;
    } 
    
    html += `</table>`; 
    
    return html; 
}

function executarExecucao() {
    const tipo = document.getElementById("tipo-execucao").value;
    const tamanhoInput = document.getElementById("op-aleatorio").value;
 
    let tamanho;

    if (tipo === "aleatorio") {
        if (!tamanhoInput || parseInt(tamanhoInput) < 1) {
            alert("Por favor, insira um número válido para o tamanho do problema (maior que 0)!");
            return;
        } else {
            tamanho = parseInt(tamanhoInput);
        }
    }

    fetch("/metodos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tipo, tamanho })
    })
    .then(res => res.json())
    .then(data => {
        const resultado = document.getElementById("resultado-metodo");
        resultado.classList.remove("hidden");

        const r = data.resultado_execucao;

        // 🔥 IMPORTANTE: Salvar TODOS os dados da execução para análise posterior
        window.ultimoResultadoExecucao = {
            ...r,
            tipo,
            tamanho
        };

        console.log("🔥 Execução salva para análise:", window.ultimoResultadoExecucao);

        // Tabela Turnos dos técnicos
        let tabelaTurnos = `<h3>Turnos dos Técnicos</h3><table><tr><th>Técnico</th><th>Turno</th></tr>`;
        for (const [tec, turno] of Object.entries(r["Turnos dos técnicos"])) {
            tabelaTurnos += `<tr><td>${tec}</td><td>${turno}</td></tr>`;
        }
        tabelaTurnos += "</table>";

        // Tabela Tempo para manutenção
        let todas_maquinas = new Set();
        for (const tempos of Object.values(r["Tempo para manutenção"])) {
            Object.keys(tempos).forEach(m => todas_maquinas.add(m));
        }
        todas_maquinas = Array.from(todas_maquinas).sort();

        let tabelaTempo = `<h3>Tempo para Manutenção</h3><div class="scroll-table"><table><tr><th>Técnico</th>`;
        todas_maquinas.forEach(m => tabelaTempo += `<th>${m}</th>`);
        tabelaTempo += `</tr>`;
        for (const [tec, tempos] of Object.entries(r["Tempo para manutenção"])) {
            tabelaTempo += `<tr><td>${tec}</td>`;
            todas_maquinas.forEach(m => tabelaTempo += `<td>${tempos[m] !== undefined ? tempos[m] : "-"}</td>`);
            tabelaTempo += `</tr>`;
        }
        tabelaTempo += "</table></div>";

        // Turnos Permitidos
        let tabelaTurnosPermitidos = `<h3>Turnos Permitidos por Máquina</h3><table><tr><th>Máquina</th><th>Turnos Permitidos</th></tr>`;
        for (const [m, turnos] of Object.entries(r["Turnos permitidos"])) {
            tabelaTurnosPermitidos += `<tr><td>${m}</td><td>${turnos.join(", ")}</td></tr>`;
        }
        tabelaTurnosPermitidos += "</table>";

        // Solução Inicial
        let tabelaSolucao = `<h3>Solução Inicial</h3><table><tr><th>Técnico</th><th>Máquinas</th></tr>`;
        for (const [tec, maquinas] of Object.entries(r["Solução inicial"])) {
            tabelaSolucao += `<tr><td>${tec}</td><td>${maquinas.join(", ")}</td></tr>`;
        }
        tabelaSolucao += "</table>";

        // Horas Trabalhadas
        let tabelaCarga = `<h3>Horas Trabalhadas por Técnico</h3><table><tr><th>Técnico</th><th>Horas</th></tr>`;
        for (const [tec, horas] of Object.entries(r["Horas trabalhadas"])) {
            tabelaCarga += `<tr><td>${tec}</td><td>${horas}</td></tr>`;
        }
        tabelaCarga += "</table>";

        resultado.innerHTML = `
            ${tabelaTurnos}
            ${tabelaTempo}
            ${tabelaTurnosPermitidos}
            ${tabelaSolucao}
            ${tabelaCarga}
            <p><b>Custo da solução inicial:</b> ${r["Custo da solução inicial"]}</p>
            <p><b>Máquinas não atribuídas:</b> ${r["Máquinas não atribuídas"].join(", ") || "Nenhuma"}</p>
        `;
    });
}

// Função para visualizar a imagem antes de upload
function previewImage(input, id) {
    const preview = document.getElementById('image-preview-' + id);
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            while (preview.firstChild) {
                preview.removeChild(preview.firstChild);
            }
            const img = document.createElement('img');
            img.src = e.target.result;
            img.alt = 'Foto do discente';
            preview.appendChild(img);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// Mostrar label aleatorio quando for escolhido o metodo aleatorio
document.getElementById('tipo-execucao').addEventListener('change', function() {
    const opcao = document.getElementById('opcao-aleatorio');
    if (this.value === 'aleatorio') {
        opcao.classList.remove("hidden")
    } else {
        opcao.classList.add("hidden")
    }
});

// Exibir os campos adicionais conforme o método escolhido
document.getElementById('metodo').addEventListener('change', function () {
    const metodo = this.value;

    const camposContainer = document.getElementById('campos-metodo');
    const subidaTentativas = document.getElementById('campos-subida-tentativas');
    const tempera = document.getElementById('campos-tempera');

    camposContainer.classList.add('hidden');
    subidaTentativas.classList.add('hidden');
    tempera.classList.add('hidden');

    if (metodo === 'subida-tentativas') {
        camposContainer.classList.remove('hidden');
        subidaTentativas.classList.remove('hidden');
    } else if (metodo === 'tempera') {
        camposContainer.classList.remove('hidden');
        tempera.classList.remove('hidden');
    }
});

// Função para o botão análise dos métodos
async function analisarMetodos() {
    if (!window.ultimoResultadoExecucao) {
        alert("Primeiro gere a solução inicial!");
        return;
    }

    const dados = {
        solucao_inicial: window.ultimoResultadoExecucao["Solução inicial"],
        tempo: window.ultimoResultadoExecucao["Tempo para manutenção"],
        limite_horas: window.ultimoResultadoExecucao["Limite de horas"],
        num_tentativas: document.getElementById("num-tentativas")?.value || 10,
        temp_ini: document.getElementById("temp-inicial")?.value || 50,
        temp_fim: document.getElementById("temp-final")?.value || 1,
        fator: document.getElementById("fator-redutor")?.value || 0.95
    };

    const resposta = await fetch("/analise", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
    });

    const resultado = await resposta.json();
    
    mostrarTabelaAnalise(resultado.resultados);
}

function mostrarTabelaAnalise(resultados) {
    let div = document.getElementById("resultado-metodo");
    div.classList.remove("hidden");

    let tabela = `
    <h3>Resultado da Análise dos Métodos</h3>
    <table border="1" cellpadding="6">
        <tr>
            <th>Método</th>
            <th>Solução Inicial</th>
            <th>Solução Final</th>
            <th>Ganho (%)</th>
            <th>Tempo Execução</th>
        </tr>
    `;

    resultados.forEach(r => {
        tabela += `
        <tr>
            <td>${r["Método"]}</td>
            <td>${r["Solução Inicial"]}</td>
            <td>${r["Solução Final"]}</td>
            <td>${r["Ganho (%)"]}</td>
            <td>${r["Tempo Execução"]}</td>
        </tr>
        `;
    });

    tabela += "</table>";

    div.innerHTML = tabela;
}

// Melhorar a experiência em dispositivos móveis
document.addEventListener('DOMContentLoaded', function() {
    function adjustViewport() {
        let vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    adjustViewport();
    window.addEventListener('resize', adjustViewport);

    if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
        const inputs = document.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                document.body.style.zoom = '0.99';
            });
            input.addEventListener('blur', () => {
                document.body.style.zoom = '1';
            });
        });
    }
});

document.getElementById("btn-executar-ag").addEventListener("click", async () => {
    if (!window.ultimoResultadoExecucao) {
        alert("Primeiro gere a solução inicial!");
        return;
    }

    let payload = {
    solucao_inicial: window.ultimoResultadoExecucao["Solução inicial"],
    tempo: window.ultimoResultadoExecucao["Tempo para manutenção"],
    turnos_tecnicos: window.ultimoResultadoExecucao["Turnos dos técnicos"],
    turnos_permitidos: window.ultimoResultadoExecucao["Turnos permitidos"],
    limite_horas: window.ultimoResultadoExecucao["Limite de horas"],
    tam_pop: parseInt(document.getElementById("tam-pop").value),
    num_geracoes: parseInt(document.getElementById("num-geracoes").value),
    taxa_cross: parseFloat(document.getElementById("taxa-crossover").value),
    taxa_mut: parseFloat(document.getElementById("taxa-mutacao").value)
};


    try {
        const resp = await fetch("/executar_ag", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const dados = await resp.json();

        document.getElementById("resultado-ag").classList.remove("hidden");
        document.getElementById("resultado-ag").innerHTML = `
            <h3>Resultado AG</h3>
            <p><strong>Custo final:</strong> ${dados.custo_final}</p>
            ${montarTabela(dados.solucao_final)}
        `;
    } catch (err) {
        console.error(err);
        alert("Ocorreu um erro ao executar o AG.");
    }
});

// Função para montar tabela de solução (técnico x máquinas)
function montarTabela(solucao) { 
    let html = `
        <table border="1" cellpadding="6" style="border-collapse: collapse; margin-bottom: 20px;">
            <tr style="background:#eee;">
                <th>Técnico</th>
                <th>Máquinas</th>
            </tr>
    `;
    for (const tecnico in solucao) { 
        const maquinas = solucao[tecnico]; 
        html += `
            <tr>
                <td><strong>${tecnico}</strong></td>
                <td>${maquinas.length > 0 ? maquinas.join(", ") : ""}</td>
            </tr>
        `;
    } 
    html += "</table>"; 
    return html; 
}