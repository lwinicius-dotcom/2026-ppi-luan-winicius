from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('colecao', __name__)

@bp.route('/')
def index():
    db = get_db()
    # Lista apenas os objetos do usuário logado (ou você pode remover o WHERE se quiser mostrar de todos)
    objetos = db.execute(
        'SELECT o.id, nome, categoria, descricao, valor_estimado, data_aquisicao, usuario_id, username'
        ' FROM objeto o JOIN user u ON o.usuario_id = u.id'
        ' ORDER BY data_aquisicao DESC'
    ).fetchall()
    return render_template('colecao/index.html', objetos=objetos)

@bp.route('/criar', methods=('GET', 'POST'))
@login_required
def criar():
    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        descricao = request.form['descricao']
        valor_estimado = request.form['valor_estimado']
        db = get_db()
        error = None

        if not nome:
            error = 'O nome do objeto é obrigatório.'
        if not categoria:
            error = 'A categoria é obrigatória.'

        if error is None:
            db.execute(
                'INSERT INTO objeto (nome, categoria, descricao, valor_estimado, usuario_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (nome, categoria, descricao, valor_estimado, g.user['id'])
            )
            db.commit()
            return redirect(url_for('colecao.index'))

        flash(error)

    return render_template('colecao/criar.html')

def get_objeto(id, check_author=True):
    objeto = get_db().execute(
        'SELECT id, nome, categoria, descricao, valor_estimado, usuario_id'
        ' FROM objeto WHERE id = ?',
        (id,)
    ).fetchone()

    if objeto is None:
        abort(404, f"Objeto com ID {id} não existe.")

    if check_author and objeto['usuario_id'] != g.user['id']:
        abort(403)

    return objeto

@bp.route('/<int:id>/editar', methods=('GET', 'POST'))
@login_required
def editar(id):
    objeto = get_objeto(id)

    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        descricao = request.form['descricao']
        valor_estimado = request.form['valor_estimado']
        db = get_db()
        error = None

        if not nome:
            error = 'O nome do objeto é obrigatório.'

        if error is None:
            db.execute(
                'UPDATE objeto SET nome = ?, categoria = ?, descricao = ?, valor_estimado = ?'
                ' WHERE id = ?',
                (nome, categoria, descricao, valor_estimado, id)
            )
            db.commit()
            return redirect(url_for('colecao.index'))

        flash(error)

    return render_template('colecao/editar.html', objeto=objeto)

@bp.route('/<int:id>/deletar', methods=('POST',))
@login_required
def deletar(id):
    get_objeto(id)
    db = get_db()
    db.execute('DELETE FROM objeto WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('colecao.index'))