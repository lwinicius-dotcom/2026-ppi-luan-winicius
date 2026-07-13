import os
from flaskr import Flask  

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, template_folder='../templates')
    SECRET_KEY='chave_secreta_para_seu_acervo',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return '<h1>📦 Página Inicial Provisória (Prática 05)</h1><p>Banco de dados e Autenticação configurados!</p>'

    return app