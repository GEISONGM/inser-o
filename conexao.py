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

def buscaContatos(cursor):
    cursor.execute("select * from contatos")
    contatos = cursor.fetchall()
    for contato in contatos:
        print(contato)

def main():
    conexao = conectarBd()
    if conexao:
        cursor = conexao.cursor()
        buscaContatos(cursor)

if __name__ == "__main__":
    main()
