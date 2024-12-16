from flask import Flask, render_template, request
import mysql.connector

def conectarBd():
    try:
        # Conexão com o banco de dados
        conexao = mysql.connector.connect(
            host="localhost",  # Endereço do servidor
            user="root",  # Usuário do banco
            password="",  # Senha do banco
            database="sistemagerenciamento"  # Nome do banco que contém a tabela
        )
        return conexao     
    except mysql.connector.Error as err:
        print(f"Erro ao acessar a tabela: {err}")
        return None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuario', methods=['POST'])
def salvarUsuario(): 
    nome = request.form.get('nome')
    email = request.form.get('email')

    conexao = conectarBd()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
        conexao.commit()
        conexao.close() 
        return sucesso(), 200 
    else:
        return erro("Erro ao conectar ao banco de dados!"), 500

@app.route('/usuario', methods=['GET'])
def buscaListaUsuarios():
    conexao = conectarBd()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios")
        resultados = cursor.fetchall()
        usuarios = [list(usuario) for usuario in resultados]
        conexao.close() 
        return usuarios, 200 

@app.route('/cadastrar-contato', methods=['POST'])
def salvarContato(): 
    usuario_id = request.form.get('usuario_id')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')
    conexao = conectarBd()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO contatos (usuario_id, telefone, endereco) VALUES (%s, %s, %s)", (usuario_id, telefone, endereco))
        conexao.commit()
        conexao.close() 
        return sucesso(), 200 
    else:
        return erro("Erro ao conectar ao banco de dados!"), 500

@app.route('/contatos-busca-um', methods=['GET'])
def buscarContatoPorUsuario():
    usuario_id = request.args.get('usuario_id')

    conexao = conectarBd()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT usuario_id, telefone, endereco FROM contatos WHERE usuario_id = %s", (usuario_id,))
        resultado = cursor.fetchall()
        if resultado:
            usuario = [list(usuario) for usuario in resultado]
            conexao.close()
            return usuario[0], 200 
        else:
            conexao.close() 
            return [], 200
    else:
        return erro("Erro ao conectar ao banco de dados!"), 500

@app.route('/contato/deletar', methods=['DELETE'])
def deletarContato():
    usuario_id = request.args.get('usuario_id')

    conexao = conectarBd()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, usuario_id, telefone, endereco FROM contatos WHERE usuario_id = %s", (usuario_id,))
        resultado = cursor.fetchall()
        if resultado:
            contato = [list(usuario) for usuario in resultado][0]
            cursor.execute("DELETE FROM contatos WHERE id = %s", (contato[0],)) 
            conexao.commit()
            conexao.close()
            return {}, 200  
        else:
            conexao.close() 
            return erro("Contato nao encontrado"), 200 
    else:
        return erro("Erro ao conectar ao banco de dados!"), 500

def erro(msn):
    return {erro: msn}

def sucesso():
    return"""
        <html>
            <head><title>Sucesso</title></head>
            <body>
                <h1>Dados salvo com sucesso</h1>
                <a href="../">Voltar a tela anterior</a>
            </body>
        </html>
    """
def sucessoDeletar():
    return"""
        <html>
            <head><title>Sucesso</title></head>
            <body>
                <h1>Dados salvo com sucesso</h1>
                <a href="../">Voltar a tela anterior</a>
            </body>
        </html>
    """

if __name__ == "__main__":
    app.run(debug=True)