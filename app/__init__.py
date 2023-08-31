
from flask import Flask, render_template, send_from_directory
from dotenv import load_dotenv
import os

from app.API import api
from app.models import db, ma

# -------------------------------------GLOBAL EXTENTIONS-----------------------------------
# Database migrations
from flask_migrate import Migrate
migrate = Migrate()
from app.models.users import User
# login manager
from flask_login import LoginManager
login_manager = LoginManager()
# Gravatar
from flask_gravatar import Gravatar
gravatar = Gravatar(size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)
# JWT
from flask_jwt_extended import JWTManager
jwt = JWTManager()



def create_app():
    # load environment variables
    app = Flask(__name__)
    APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(APP_ROOT, ".env")
    load_dotenv(dotenv_path)

    app.config.from_object('config.settings.' + os.environ.get('FLASK_ENV'))

    # -------------------------------INITIALIZE EXTENTIONS----------------------------------
    # sqlalchemy
    db.init_app(app)
    # marshmallow
    ma.init_app(app)
    # restful
    api.init_app(app)
    # migrate
    migrate.init_app(app)
    # login manager
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    # gravatar
    gravatar.init_app(app)
    # jwt
    jwt.init_app(app)




    
    # ----------------------------------APP CONTEXT----------------------------------
    with app.app_context():
        # Database initiation
        from app.models import users,posts
        db.create_all()
        db.session.commit()


        # user loader
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # handling error codes
        @app.errorhandler(404)
        def not_found(error):
            return render_template('errors/404.html',title='404'),

        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(os.path.join(app.root_path, 'static/images'),'favicon.ico', mimetype='image/vnd.microsoft.icon')
        
        # register blueprints
        from app.views.home import home as home_blueprint
        app.register_blueprint(home_blueprint)

        from app.views.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)


        # return the app to run it
        return app






