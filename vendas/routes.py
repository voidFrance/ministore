# vendas/routes.py
from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection
import mysql.connector


vendas_bp = Blueprint('vendas', __name__, template_folder='templates')


def _carregar_clientes(cursor):
    cursor.execute('SELECT id, nome FROM clientes ORDER BY nome')
    return cursor.fetchall()


def _carregar_produtos(cursor):
    cursor.execute('SELECT id, codigo, nome, preco FROM produtos ORDER BY nome')
    return cursor.fetchall()


def _itens_do_formulario(form):
    """Le os pares produto/quantidade do formulario, descartando linhas vazias."""
    ids = form.getlist('id_produto')
    quantidades = form.getlist('quantidade')
    itens = []
    for bruto_id, bruto_qtd in zip(ids, quantidades):
        if not bruto_id:
            continue
        try:
            id_produto = int(bruto_id)
            qtd = int(bruto_qtd)
        except (TypeError, ValueError):
            raise ValueError('Produto ou quantidade invalidos.')
        if qtd <= 0:
            raise ValueError('Quantidade precisa ser maior que zero.')
        itens.append((id_produto, qtd))
    return itens


@vendas_bp.route('/vendas')
def listar():
    conn = None
    cursor = None
    vendas = []
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT v.id, v.data_venda, v.total, c.nome AS cliente,
                   COUNT(i.id) AS total_itens
            FROM vendas v
            JOIN clientes c ON c.id = v.id_cliente
            LEFT JOIN itens_venda i ON i.id_venda = v.id
            GROUP BY v.id, v.data_venda, v.total, c.nome
            ORDER BY v.data_venda DESC, v.id DESC
        ''')
        vendas = cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f'Erro ao buscar vendas: {e}', 'danger')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return render_template('vendas/lista.html', vendas=vendas)


@vendas_bp.route('/vendas/nova', methods=['GET', 'POST'])
def nova():
    conn = None
    cursor = None
    clientes = []
    produtos = []
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        clientes = _carregar_clientes(cursor)
        produtos = _carregar_produtos(cursor)

        if request.method == 'POST':
            id_cliente = request.form.get('id_cliente')
            if not id_cliente:
                raise ValueError('Selecione o cliente da venda.')

            itens = _itens_do_formulario(request.form)
            if not itens:
                raise ValueError('Inclua ao menos um item na venda.')

            # Preço vem do banco, nunca do formulário: cliente pode forjar o valor.
            marcadores = ', '.join(['%s'] * len({i for i, _ in itens}))
            cursor.execute(
                f'SELECT id, preco FROM produtos WHERE id IN ({marcadores})',
                tuple({i for i, _ in itens})
            )
            precos = {linha['id']: linha['preco'] for linha in cursor.fetchall()}
            faltando = [i for i, _ in itens if i not in precos]
            if faltando:
                raise ValueError(f'Produto inexistente: id {faltando[0]}.')

            linhas = [(id_produto, qtd, precos[id_produto]) for id_produto, qtd in itens]
            total = sum((preco * qtd for _, qtd, preco in linhas), Decimal('0.00'))

            cursor.execute(
                'INSERT INTO vendas (id_cliente, total) VALUES (%s, %s)',
                (id_cliente, total)
            )
            id_venda = cursor.lastrowid
            cursor.executemany(
                '''INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario)
                   VALUES (%s, %s, %s, %s)''',
                [(id_venda, id_produto, qtd, preco)
                 for id_produto, qtd, preco in linhas]
            )
            conn.commit()
            flash(f'Venda #{id_venda} registrada com sucesso!', 'success')
            return redirect(url_for('vendas.detalhe', id=id_venda))

    except ValueError as e:
        flash(str(e), 'warning')
    except mysql.connector.Error as e:
        if conn:
            conn.rollback()
        flash(f'Erro ao registrar venda: {e}', 'danger')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('vendas/form.html', clientes=clientes, produtos=produtos,
                           form=request.form)


@vendas_bp.route('/vendas/<int:id>')
def detalhe(id):
    conn = None
    cursor = None
    venda = None
    itens = []
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT v.id, v.data_venda, v.total, v.id_cliente,
                   c.nome AS cliente, c.email, c.telefone
            FROM vendas v
            JOIN clientes c ON c.id = v.id_cliente
            WHERE v.id = %s
        ''', (id,))
        venda = cursor.fetchone()
        if not venda:
            flash('Venda não encontrada.', 'danger')
            return redirect(url_for('vendas.listar'))

        cursor.execute('''
            SELECT i.id, i.quantidade, i.preco_unitario,
                   i.quantidade * i.preco_unitario AS subtotal,
                   p.nome AS produto, p.codigo
            FROM itens_venda i
            JOIN produtos p ON p.id = i.id_produto
            WHERE i.id_venda = %s
            ORDER BY i.id
        ''', (id,))
        itens = cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f'Erro ao abrir venda: {e}', 'danger')
        return redirect(url_for('vendas.listar'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('vendas/detalhe.html', venda=venda, itens=itens)


@vendas_bp.route('/vendas/<int:id>/excluir', methods=['POST'])
def excluir(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # itens_venda tem FK para vendas: apaga os filhos antes do pai.
        cursor.execute('DELETE FROM itens_venda WHERE id_venda = %s', (id,))
        cursor.execute('DELETE FROM vendas WHERE id = %s', (id,))
        conn.commit()
        flash(f'Venda #{id} excluída.', 'success')
    except mysql.connector.Error as e:
        if conn:
            conn.rollback()
        flash(f'Erro ao excluir venda: {e}', 'danger')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return redirect(url_for('vendas.listar'))
