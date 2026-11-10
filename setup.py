# setup_db.py
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123mudar'
)

cursor = conn.cursor()

cursor.execute("""
    CREATE DATABASE IF NOT EXISTS ministore
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci
""")

cursor.execute("USE ministore")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(100),
        telefone VARCHAR(20),
        cpf VARCHAR(14),
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        descricao TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        codigo VARCHAR(50) NOT NULL,
        nome VARCHAR(100) NOT NULL,
        descricao TEXT,
        preco DECIMAL(10,2) NOT NULL,
        id_categoria INT,
        FOREIGN KEY (id_categoria) REFERENCES categorias(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        id_cliente INT NOT NULL,
        data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
        total DECIMAL(10,2) NOT NULL DEFAULT 0,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens_venda (
        id INT AUTO_INCREMENT PRIMARY KEY,
        id_venda INT NOT NULL,
        id_produto INT NOT NULL,
        quantidade INT NOT NULL,
        preco_unitario DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (id_venda) REFERENCES vendas(id),
        FOREIGN KEY (id_produto) REFERENCES produtos(id)
    )
""")

cursor.execute("""
    CREATE USER IF NOT EXISTS 'ministore'@'localhost'
    IDENTIFIED BY '123mudar'
""")

cursor.execute("""
    GRANT ALL PRIVILEGES ON ministore.* TO 'ministore'@'localhost'
""")

cursor.execute("FLUSH PRIVILEGES")

cursor.close()
conn.close()

print("Banco de dados criado com sucesso!")
