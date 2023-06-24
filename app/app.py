from sqlalchemy import select
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_moment import Moment


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
moment = Moment()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'bp_auth.login'
    login_manager.login_message_category = 'info'
    moment.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        id = int(user_id)
        return db.session.get(User, id)

    from .bp_views import bp_views
    app.register_blueprint(bp_views)

    from .bp_auth import bp_auth
    app.register_blueprint(bp_auth)

    # error handling
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(403)
    def permission_denied(e):
        return render_template('403.html'), 403

    return app