# produtos/routes.py
from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection
import mysql.connector


produtos_bp = Blueprint('produtos', __name__, template_folder='templates')


def _preco(valor):
    """Converte o texto do formulario em Decimal, recusando lixo e valor negativo."""
    try:
        preco = Decimal(valor.replace(',', '.'))
    except (InvalidOperation, AttributeError):
        raise ValueError('Preco invalido.')
    if preco < 0:
        raise ValueError('Preco nao pode ser negativo.')
    return preco


def _categorias(cursor):
    cursor.execute('SELECT id, nome FROM categorias ORDER BY nome')
    return cursor.fetchall()


@produtos_bp.route('/produtos')
def listar():
    conn = None
    cursor = None
    produtos = []
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT p.id, p.codigo, p.nome, p.descricao, p.preco,
                   p.id_categoria, c.nome AS categoria
            FROM produtos p
            LEFT JOIN categorias c ON c.id = p.id_categoria
            ORDER BY p.nome
        ''')
        produtos = cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f'Erro ao buscar produtos: {e}', 'danger')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return render_template('produtos/lista.html', produtos=produtos)


@produtos_bp.route('/produtos/novo', methods=['GET', 'POST'])
def novo():
    conn = None
    cursor = None
    categorias = []
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        categorias = _categorias(cursor)

        if request.method == 'POST':
            codigo = request.form['codigo'].strip()
            nome = request.form['nome'].strip()
            descricao = request.form.get('descricao', '').strip()
            id_categoria = request.form.get('id_categoria') or None
            try:
                preco = _preco(request.form.get('preco', ''))
            except ValueError as e:
                flash(str(e), 'warning')
                return render_template('produtos/form.html', produto=request.form,
                                       categorias=categorias)

            cursor.execute('''
                INSERT INTO produtos (codigo, nome, descricao, preco, id_categoria)
                VALUES (%s, %s, %s, %s, %s)
            ''', (codigo, nome, descricao, preco, id_categoria))
            conn.commit()
            flash('Produto cadastrado com sucesso!', 'success')
            return redirect(url_for('produtos.listar'))
    except mysql.connector.Error as e:
        flash(f'Erro ao cadastrar produto: {e}', 'danger')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return render_template('produtos/form.html', produto=None, categorias=categorias)


@produtos_bp.route('/produtos/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        categorias = _categorias(cursor)

        if request.method == 'POST':
            codigo = request.form['codigo'].strip()
            nome = request.form['nome'].strip()
            descricao = request.form.get('descricao', '').strip()
            id_categoria = request.form.get('id_categoria') or None
            try:
                preco = _preco(request.form.get('preco', ''))
            except ValueError as e:
                flash(str(e), 'warning')
                return render_template('produtos/form.html', produto=request.form,
                                       categorias=categorias)

            cursor.execute('''
                UPDATE produtos
                SET codigo=%s, nome=%s, descricao=%s, preco=%s, id_categoria=%s
                WHERE id=%s
            ''', (codigo, nome, descricao, preco, id_categoria, id))
            conn.commit()
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('produtos.listar'))

        cursor.execute('SELECT * FROM produtos WHERE id = %s', (id,))
        produto = cursor.fetchone()
        if not produto:
            flash('Produto não encontrado.', 'danger')
            return redirect(url_for('produtos.listar'))
    except mysql.connector.Error as e:
        flash(f'Erro: {e}', 'danger')
        return redirect(url_for('produtos.listar'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('produtos/form.html', produto=produto, categorias=categorias)


@produtos_bp.route('/produtos/<int:id>/excluir', methods=['POST'])
def excluir(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM produtos WHERE id = %s', (id,))
        conn.commit()
        flash('Produto excluído com sucesso!', 'success')
    except mysql.connector.IntegrityError:
        flash('Produto usado em alguma venda. Exclua a venda antes.', 'warning')
    except mysql.connector.Error as e:
        flash(f'Erro ao excluir produto: {e}', 'danger')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return redirect(url_for('produtos.listar'))
