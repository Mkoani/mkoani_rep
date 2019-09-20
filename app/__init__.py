import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, IMAGES, configure_uploads

from config import Config

app = Flask(__name__)

# initialise flask_bootstrap
bootstrap = Bootstrap(app)

# initialise flask login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# initialise flask uploads
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/app/static/images'
app.config['UPLOADED_PHOTOS_URL'] = '../static/images/'
configure_uploads(app, photos)

# tells flask where the configuration data is
app.config.from_object(Config)

# create sqlalchemy instance
db = SQLAlchemy(app)

# setup mail
mail = Mail(app)

# create a migration repository
migrate = Migrate(app, db)

from app.customer import routes
from app.owner.main import routes
from app.owner.auth import routes
from app import models
