console.log("pagina criada com sucesso")

function showTab(tab) {
    document.getElementById('tab-usuario').classList.remove('active-tab');
    document.getElementById('tab-contato').classList.remove('active-tab');
    document.getElementById('content-usuario').classList.remove('active-content');
    document.getElementById('content-contato').classList.remove('active-content');
    console.log(tab)
    // Mostrar o conteúdo da aba selecionada
    if (tab === 'usuario') {
        document.getElementById('content-usuario').classList.add('active-content');
        document.getElementById('tab-usuario').classList.add('active-tab');
    } else {
        document.getElementById('content-contato').classList.add('active-content');
        document.getElementById('tab-contato').classList.add('active-tab');
    }
}

function buscarDadosUsuarios() {
    // URL da API
    const apiUrl = 'http://127.0.0.1:5000/usuario'; // Exemplo de API pública

    // Usando fetch para fazer a requisição GET
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na requisição: ' + response.status);
            }
            return response.json();  // Converte a resposta para JSON
        })
        .then(data => {
            console.log('Dados recebidos:', data);  // Exibe os dados no console
            const dadosFormatados = data.map(usuario => {
                return {
                    id: usuario[0],
                    nome: usuario[1]
                }
            })
            // Aqui você pode manipular os dados, por exemplo, exibir na página
            const selectUsuario = document.getElementById('usuario_id');
            preencheFormulario(selectUsuario);

            for (let i = 0; i < dadosFormatados.length; i++) {
                // Criando um elemento <option>
                const opcao = document.createElement('option');
                opcao.value = dadosFormatados[i].id;
                opcao.textContent = dadosFormatados[i].nome; 
    
                // Adicionando a opção criada ao <select>
                selectUsuario.appendChild(opcao);
            }
        })
        .catch(error => {
            console.error('Erro:', error);  // Exibe erros no console
        });
}

function preencheFormulario(selectUsuario) {
    selectUsuario.addEventListener("change", async function () {
        const apiUrl = `http://127.0.0.1:5000/contatos-busca-um?usuario_id=${selectUsuario.value}`
        const response = await fetch(apiUrl);
        const data = await response.json();
        const campoTelefone = document.getElementById('telefone');
        const campoEndereco = document.getElementById('endereco');
        if(data.length) {
            const dadosFormatados = {
                id: data[0],
                telefone: data[1],
                endereco: data[2]
            }
            campoTelefone.value = dadosFormatados?.telefone
            campoEndereco.value = dadosFormatados?.endereco
        }else {
            campoTelefone.value = '';
            campoEndereco.value = '';
        }
    })
}

async function deletarContato() {
    const selectUsuario = document.getElementById('usuario_id');
    const apiUrl = `http://127.0.0.1:5000/contato/deletar?usuario_id=${selectUsuario.value}`
    const response = await fetch(apiUrl, {method: 'DELETE'});
    const data = await response.json();
    if(data) {
        const campoTelefone = document.getElementById('telefone');
        const campoEndereco = document.getElementById('endereco');
        selectUsuario.value = 0;
        campoTelefone.value = '';
        campoEndereco.value = '';
    }
}

buscarDadosUsuarios()