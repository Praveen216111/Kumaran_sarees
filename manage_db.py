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
            blue_chudi = Product.query.filter_by(name='Sky Blue Cotton Saree Without Blouse3').first()
            if blue_chudi:
                logger.debug("Deleting Blue Cotton Chudi")
                db.session.delete(blue_chudi)
                db.session.commit()
            else:
                logger.debug("Blue Cotton Chudi not found")
        except Exception as e:
            logger.error(f"Error deleting Blue Cotton Chudi: {e}")

def add_products():
    with app.app_context():
        try:
            products = [
                {
                    'name': 'Pink Cotton Saree Without Blouse1',
                    'category': 'Cotton Saree',
                    'fabric': 'Cotton',
                    'price': 500.0,
                    'stock': 2,
                    'image_path': '/static/images/products/pink_cotton_saree_without_blouse.jpg'
                },
                {
                    'name': 'Rose Cotton Saree Without Blouse2',
                    'category': 'Cotton Saree',
                    'fabric': 'Cotton',
                    'price': 500.0,
                    'stock': 2,
                    'image_path': '/static/images/products/rose_cotton_saree_without_blouse.jpg'
                },
                {
                    'name': 'Sky Blue Cotton Saree Without Blouse3',
                    'category': 'Cotton Saree',
                    'fabric': 'Cotton',
                    'price': 500.0,
                    'stock': 2,
                    'image_path': '/static/images/products/sky_blue_cotton_saree_without_blouse3.jpg'
                },
                {
                    'name': 'Sky Blue Cotton Saree With Blouse',
                    'category': 'Cotton Saree',
                    'fabric': 'Cotton',
                    'price': 700.0,
                    'stock': 2,
                    'image_path': '/static/images/products/sky_blue_cotton_saree_with_blouse.jpg'
                },
                {
                    'name': 'Sky Blue Cotton Saree With Blouse1',
                    'category': 'Cotton Saree',
                    'fabric': 'Cotton',
                    'price': 700.0,
                    'stock': 2,
                    'image_path': '/static/images/products/sky_blue_cotton_saree_with_blouse2.jpg'
                },
                {
                    'name': 'Sky Blue Cotton Saree With Blouse2',
                    'category': 'Cotton Saree',
                    'fabric': 'Cotton',
                    'price': 700.0,
                    'stock': 2,
                    'image_path': '/static/images/products/sky_blue_cotton_saree_with_blouse3.jpg'
                },
                {
                    'name': 'Yellow Cotton Saree With Blouse',
                    'category': 'Cotton Saree',
                    'fabric': 'Cotton',
                    'price': 700.0,
                    'stock': 2,
                    'image_path': '/static/images/products/yellow_cotton_saree_with_blouse.jpg'
                },
                {
                    'name': 'Yellow Cotton Saree Without Blouse',
                    'category': 'Cotton Saree',
                    'fabric': 'Cotton',
                    'price': 500.0,
                    'stock': 2,
                    'image_path': '/static/images/products/yellow_cotton_saree_without_blouse.jpg'
                },
                {
                    'name': 'Yellow Cotton Saree Without Blouse1',
                    'category': 'Cotton Saree',
                    'fabric': 'Cotton',
                    'price': 500.0,
                    'stock': 2,
                    'image_path': '/static/images/products/yellow_cotton_saree_without_blouse1.jpg'
                }
            ]
            for product_data in products:
                if not Product.query.filter_by(name=product_data['name']).first():
                    new_product = Product(**product_data)
                    db.session.add(new_product)
                    logger.debug(f"Added {product_data['name']}")
            db.session.commit()
        except Exception as e:
            logger.error(f"Error adding products: {e}")
            db.session.rollback()

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
    add_products()