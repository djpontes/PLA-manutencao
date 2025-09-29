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


// Função para executar o método selecionado
function executarMetodo() {
    const metodo = document.getElementById("metodo").value;
    if (!metodo) {
        alert("Por favor, escolha um método válido!");
        return;
    }

    const resultado = document.getElementById("resultado-metodo");
    resultado.classList.remove("hidden");
    resultado.innerHTML = "<h3>Processando...</h3>";

    setTimeout(() => {
        resultado.innerHTML = `
            <h3>Resultado:</h3>
            <p>Módulo em desenvolvimento</p>
        `;
    }, 1000);
}

function executarExecucao() {
    const tipo = document.getElementById("tipo-execucao").value;
    const tamanhoInput = document.getElementById("op-aleatorio").value;
 
    let tamanho;

    if (tipo === "aleatorio") {
        if (!tamanhoInput || parseInt(tamanhoInput) < 1) {
            alert("Por favor, insira um número válido para o tamanho do problema (maior que 0)!");
            return; // interrompe a execução se inválido
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

        // Tabela Turnos dos técnicos
        let tabelaTurnos = `<h3>Turnos dos Técnicos</h3><table><tr><th>Técnico</th><th>Turno</th></tr>`;
        for (const [tec, turno] of Object.entries(r["Turnos dos técnicos"])) {
            tabelaTurnos += `<tr><td>${tec}</td><td>${turno}</td></tr>`;
        }
        tabelaTurnos += "</table>";

        // Tabela Tempo para manutenção
        let tabelaTempo = `<h3>Tempo para Manutenção</h3><table><tr><th>Técnico</th>`;
        const maquinas = Object.keys(r["Tempo para manutenção"][Object.keys(r["Tempo para manutenção"])[0]]);
        maquinas.forEach(m => tabelaTempo += `<th>${m}</th>`);
        tabelaTempo += `</tr>`;
        for (const [tec, tempos] of Object.entries(r["Tempo para manutenção"])) {
            tabelaTempo += `<tr><td>${tec}</td>`;
            maquinas.forEach(m => tabelaTempo += `<td>${tempos[m] || "-"}</td>`);
            tabelaTempo += `</tr>`;
        }
        tabelaTempo += "</table>";

        // Tabela Turnos Permitidos
        let tabelaTurnosPermitidos = `<h3>Turnos Permitidos por Máquina</h3><table><tr><th>Máquina</th><th>Turnos Permitidos</th></tr>`;
        for (const [m, turnos] of Object.entries(r["Turnos permitidos"])) {
            tabelaTurnosPermitidos += `<tr><td>${m}</td><td>${turnos.join(", ")}</td></tr>`;
        }
        tabelaTurnosPermitidos += "</table>";

        // Tabela Solução Inicial
        let tabelaSolucao = `<h3>Solução Inicial</h3><table><tr><th>Técnico</th><th>Máquinas</th></tr>`;
        for (const [tec, maquinas] of Object.entries(r["Solução inicial"])) {
            tabelaSolucao += `<tr><td>${tec}</td><td>${maquinas.join(", ")}</td></tr>`;
        }
        tabelaSolucao += "</table>";

        // Tabela Horas Trabalhadas
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

// Mostrar label aleatorio quando for escolhido o metodo 'Aleatorio'
document.getElementById('tipo-execucao').addEventListener('change', function() {
    const opcao = document.getElementById('opcao-aleatorio');
    if (this.value === 'aleatorio') {
        opcao.classList.remove("hidden")
    } else {
        opcao.classList.add("hidden")
    }
});

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