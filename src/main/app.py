from dotenv import load_dotenv
from flask import Flask
from auth.auth import auth_bp
from product.product import products_bp
from order.order import orders_bp
from reward.reward import rewards_bp
from categoy.category import category_bp

from models.models import db
from . import limiter, migrate, bcrypt, jwt, mail
from .config import config
load_dotenv()

app = Flask(__name__)
app.config.from_object(config)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/flask'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_SECRET_KEY'] = 'aa9b5b2010ffcf70958992f2835122c8eb15d338675de561646ed1614e8f97bf2b8429aa84ea4cd813fd5920a6f8ef556f3e8351081bdc111af6e819f345787e'
# app.config['SECRET_KEY'] = 'f70958992f2835122c8eb15d338675ef556f3e8351081bdc111af6e'
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

# app.config['MAIL_SERVER'] = 'localhost'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = None
# app.config['MAIL_PASSWORD'] = None
# app.config['MAIL_DEFAULT_SENDER'] = 'storefront@shopify.com'


# bind the app

db.init_app(app)
limiter.init_app(app)
migrate.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
mail.init_app(app)



app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(rewards_bp, url_prefix='/rewards')
app.register_blueprint(category_bp, url_prefix='/category')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)