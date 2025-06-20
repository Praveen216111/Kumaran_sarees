from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import os
import platform
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="../templates", static_folder="../static")
# Use platform-specific database path
if platform.system() == "Windows":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sarees.db'
    db_path = os.path.join(os.getcwd(), 'sarees.db')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/sarees.db'
    db_path = '/tmp/sarees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    fabric = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(200))



@app.route('/', methods=['GET'])
def home():
    try:
        logger.debug("Entering home route")
        # Delete products with stock = 0
        sold_products = Product.query.filter(Product.stock == 0).all()
        for product in sold_products:
            try:
                logger.debug(f"Deleting sold product: {product.name}")
                db.session.delete(product)
            except Exception as e:
                logger.error(f"Error deleting product {product.name}: {e}")
        db.session.commit()
        logger.debug(f"Deleted {len(sold_products)} sold products")

        # Get featured products
        featured_products = Product.query.limit(4).all()
        logger.debug(f"Featured products: {len(featured_products)}")

        return render_template('index.html', featured_products=featured_products)
    except Exception as e:
        logger.error(f"Error in home route: {e}")
        raise

@app.route('/category/plain_saree', methods=['GET'])
def plain_saree():
    try:
        logger.debug("Entering plain_saree route")
        plain_sarees = Product.query.filter_by(category='Plain Saree').all()
        logger.debug(f"Plain sarees: {len(plain_sarees)}")
        return render_template('plain_saree.html', plain_sarees=plain_sarees)
    except Exception as e:
        logger.error(f"Error in plain_saree route: {e}")
        raise

@app.route('/category/silk_saree', methods=['GET'])
def silk_saree():
    try:
        logger.debug("Entering silk_saree route")
        silk_sarees = Product.query.filter_by(category='Silk Saree').all()
        logger.debug(f"Silk sarees: {len(silk_sarees)}")
        return render_template('silk_saree.html', silk_sarees=silk_sarees)
    except Exception as e:
        logger.error(f"Error in silk_saree route: {e}")
        raise

@app.route('/category/cotton_saree', methods=['GET'])
def cotton_saree():
    try:
        logger.debug("Entering cotton_saree route")
        cotton_sarees = Product.query.filter_by(category='Cotton Saree').all()
        logger.debug(f"Cotton sarees: {len(cotton_sarees)}")
        return render_template('cotton_saree.html', cotton_sarees=cotton_sarees)
    except Exception as e:
        logger.error(f"Error in cotton_saree route: {e}")
        raise

if __name__ == '__main__':
    app.run(debug=True)