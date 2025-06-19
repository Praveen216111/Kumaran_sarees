from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import inspect
import os
import platform
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
if platform.system() == "Windows":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sarees.db'
    db_path = os.path.join(os.getcwd(), 'sarees.db')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/sarees.db'
    db_path = '/tmp/sarees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    fabric = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(200))

def create_product_table():
    with app.app_context():
        try:
            logger.debug(f"Checking database at: {db_path}")
            if not os.path.exists(db_path):
                logger.debug("Database file does not exist, creating new one")
            db.create_all()
            if inspect(db.engine).has_table('product'):
                logger.debug("Product table created or exists")
            else:
                logger.error("Product table not created")
                raise Exception("Failed to create product table")
        except Exception as e:
            logger.error(f"Error creating product table: {e}")
            raise

def delete_blue_chudi():
    with app.app_context():
        try:
            red_saree = Product.query.filter_by(name='Rose Plain Saree').first()
            if red_saree:
                logger.debug("Deleting Blue Cotton Chudi")
                db.session.delete(red_saree)
                db.session.commit()
            else:
                logger.debug("Blue Cotton Chudi not found")
        except Exception as e:
            logger.error(f"Error deleting Blue Cotton Chudi: {e}")
def add_green_saree():
    with app.app_context():
        try:
            if not Product.query.filter_by(name='Rose Plain Saree').first():
                new_product = Product(
                    name="Rose Plain Saree",
                    category="Saree",
                    fabric="Crush Material",
                    price=700.0,
                    stock=2,
                    image_path="/static/images/products/rose_plain_saree.jpg"
                )
                db.session.add(new_product)
                db.session.commit()
                logger.debug("Added Pink Plain Saree")
            else:
                logger.debug("Pink Plain Saree already exists")
        except Exception as e:
            logger.error(f"Error adding Pink Plain Saree: {e}")

def delete_sold_sarees():
    with app.app_context():
        try:
            sold_products = Product.query.filter(Product.stock == 0).all()
            for product in sold_products:
                logger.debug(f"Deleting sold product: {product.name}")
                db.session.delete(product)
            db.session.commit()
            logger.debug(f"Deleted {len(sold_products)} sold products")
        except Exception as e:
            logger.error(f"Error deleting sold products: {e}")

if __name__ == "__main__":
    create_product_table()
    delete_blue_chudi()
    delete_sold_sarees()
    add_green_saree()
