from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"

#os.environ['GOOGLE_CLIENT_ID'] = '646560245315-bodcvrrsacfq27u1babt7s17jt7i5fma.apps.googleusercontent.com'
#os.environ['GOOGLE_CLIENT_SECRET'] = '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'

os.environ['GOOGLE_CLIENT_ID'] = '720222462733-228cv52n5m79dc0q1o2q1hritp2hv8sh.apps.googleusercontent.com'
os.environ['GOOGLE_CLIENT_SECRET'] = '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'

os.environ['SECRET_KEY'] = 'cokeoriginaltaste'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "os.environ['SECRET_KEY']"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_BINDS'] = {'spiDatabase' : f'sqlite:///spidatabase.db',
                                      'volunteerDatabase' : f'sqlite:///volunteerdatabase.db',
                                      'studentData' : f'sqlite:///studentdata.db',
                                      'admitData' : f'sqlite:///admitdata.db',
                                      'collegeDatabase' : f'sqlite:///collegedatabase.db'}

    db.init_app(app)

    from .views import views    
    from .auth import auth
    from .resultsdata import resultsdata
    from .committee_chancing import committee_chancing
    from .counselor_chancing import counselor_chancing
    from .load_data import load_data

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(resultsdata, url_prefix='/')
    app.register_blueprint(committee_chancing, url_prefix='/')
    app.register_blueprint(counselor_chancing, url_prefix='/')
    app.register_blueprint(load_data, url_prefix='/')

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



