from flask import Flask
from flask_cors import CORS

from config import Config
from .api.routes import api
from .auth.routes import auth
# from .ig.routes import ig
from .models import db, User
# from flask_migrate import Migrate
from flask_login import LoginManager
# from .models import db, User
from flask_migrate import Migrate
# from flask_moment import Moment

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
db.init_app(app)

# enabling login persistence
login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

migrate = Migrate(app, db)

login.init_app(app)

login.login_view = 'auth.login'

app.register_blueprint(auth)
app.register_blueprint(api)

from . import routes
from . import models