# dashboard/routes.py
from flask import Blueprint, render_template, flash
from database import get_connection
import mysql.connector


dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

CONTAGENS = (
    ('clientes', 'SELECT COUNT(*) FROM clientes'),
    ('categorias', 'SELECT COUNT(*) FROM categorias'),
    ('produtos', 'SELECT COUNT(*) FROM produtos'),
    ('vendas', 'SELECT COUNT(*) FROM vendas'),
)


@dashboard_bp.route('/')
def index():
    conn = None
    cursor = None
    totais = {chave: 0 for chave, _ in CONTAGENS}
    faturamento = 0
    ultimas = []
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        for chave, sql in CONTAGENS:
            cursor.execute(sql)
            linha = cursor.fetchone()
            totais[chave] = list(linha.values())[0] if linha else 0
        cursor.execute('SELECT COALESCE(SUM(total), 0) AS faturamento FROM vendas')
        faturamento = cursor.fetchone()['faturamento']
        cursor.execute('''
            SELECT v.id, v.data_venda, v.total, c.nome AS cliente
            FROM vendas v
            JOIN clientes c ON c.id = v.id_cliente
            ORDER BY v.data_venda DESC, v.id DESC
            LIMIT 5
        ''')
        ultimas = cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f'Erro ao carregar dashboard: {e}', 'danger')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('index.html', totais=totais, faturamento=faturamento,
                           ultimas=ultimas)
