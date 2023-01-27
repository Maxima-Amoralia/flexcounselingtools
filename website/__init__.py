from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

from flask_login import LoginManager

#userdb = create_engine('sqlite:///relative/path/to/userdb.db')
#userDBSession = sessionmaker(userdb)
#userdbSession = userDBSession()


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "os.environ['SECRET_KEY']"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_BINDS'] = {'spiDatabase' : f'sqlite:///spidatabase.db',
                                      'volunteerDatabase' : f'sqlite:///volunteerdatabase.db',
                                      'chancingData' : f'sqlite:///chancingdata.db',
                                      'admitData' : f'sqlite:///admitdata.db'}

    db.init_app(app)

    from .views import views    
    from .auth import auth
    from .resultsdata import resultsdata

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(resultsdata, url_prefix='/')

    from .models import User, Note, CA_Activity

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
        
    return app



