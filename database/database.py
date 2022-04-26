from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/user_records.db"  # nome da base de dados

# crie banco de dados dentro da pasta do banco de dados se nao existir
connection = connect(DB_NAME)

cursor = connection.cursor()


def create_table():
    """funcao para criar tabela dentro do banco de dados"""
    # cria usuario de tabela dentro do banco de dados se nao existir
    table_script = '''CREATE TABLE IF NOT EXISTS User(
                    full_name VARCHAR(255),
                    country VARCHAR(150)
                );
                '''
    cursor.executescript(table_script)
    connection.commit()


def insert_record(fullname, country):
    """funcao para inserir registro dentro da tabela"""
    cursor.execute("INSERT INTO User(full_name, country) VALUES(?, ?)",
                   (fullname, country))
    connection.commit()


def fetch_records():
    """funcao para buscar registros do usuario"""
    data = cursor.execute("SELECT * FROM User")
    return data


def delete_record(fullname):
    # Query para deletar usuário pelo nome
    cursor.execute("DELETE FROM User WHERE full_name = ?", (fullname, ))
    connection.commit()


def update_record(fullname, country):
    # Atualiza usuário com base no nome
    cursor.execute("UPDATE User SET full_name = ?, country= ? WHERE full_name = ?",
                   (fullname, country, fullname))
    connection.commit()
