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