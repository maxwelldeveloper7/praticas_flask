"""
    Definição de acesso ao banco de dados
"""
import sqlite3

import click
from flask import current_app, g


def get_db():
    """
        Será chamado quando o aplicativo for criado e estiver processando
        uma solicitação
    """
    if 'db' not in g:
        # Se não houver dados em armazenados em g, será atribuido
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
        verifica se uma conexão foi criada verificando se g.db foi definida.
        Se a conexão existir, ela será fechada.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
        Inicializa o banco de dados
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
        Inicializa o app
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
