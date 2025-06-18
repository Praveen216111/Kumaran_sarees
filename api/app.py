from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import platform

app = Flask(__name__, template_folder="../templates", static_folder="../static")
# Use platform-specific database path
if platform.system() == "Windows":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sarees.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/sarees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'
# Use /tmp/shorts for uploads on Vercel
app.config['UPLOAD_FOLDER'] = '/tmp/shorts' if platform.system() != "Windows" else 'static/shorts'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Max 100MB
db = SQLAlchemy(app)

# Check if upload folder exists without creating it
if platform.system() != "Windows" and not os.path.exists(app.config['UPLOAD_FOLDER']):
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError as e:
        print(f"Failed to create upload folder: {e}")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    fabric = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(200))

class Short(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_path = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_name = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Delete shorts older than 24 hours
    expiry_time = datetime.utcnow() - timedelta(hours=24)
    old_shorts = Short.query.filter(Short.uploaded_at < expiry_time).all()
    for short in old_shorts:
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(short.video_path))
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
        db.session.delete(short)
    db.session.commit()

    # Check if max 10 shorts reached for today
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    daily_shorts = Short.query.filter(Short.uploaded_at >= today).count()
    can_upload = daily_shorts < 10

    # Handle video upload
    if request.method == 'POST' and 'video' in request.files and can_upload:
        video = request.files['video']
        user_name = request.form.get('user_name')
        if video and user_name:
            if video.filename.endswith('.mp4'):
                filename = f"short_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{video.filename}"
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                try:
                    video.save(video_path)
                    # Store relative path for DB
                    db_path = f"/shorts/{filename}" if platform.system() != "Windows" else f"/static/shorts/{filename}"
                    new_short = Short(video_path=db_path, user_name=user_name)
                    db.session.add(new_short)
                    db.session.commit()
                    flash('Short uploaded successfully!', 'success')
                except OSError as e:
                    flash(f'Upload failed: {e}', 'error')
            else:
                flash('Only MP4 videos allowed!', 'error')
        else:
            flash('Please provide a name and video!', 'error')
        return redirect(url_for('home'))

    # Get categories and featured products
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    featured_products = Product.query.limit(4).all()
    shorts = Short.query.order_by(Short.uploaded_at.desc()).all()

    return render_template('index.html', categories=categories, featured_products=featured_products, shorts=shorts, can_upload=can_upload)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Product.query.first():
            db.session.add_all([
                Product(name="Red Banarasi Saree", category="Saree", fabric="searasa", price=5000, stock=10, image_path="/static/images/products/red_banarasi.jpg"),
                Product(name="Blue Cotton Chudi", category="Chudi", fabric="Cotton", price=1500, stock=25, image_path="/static/images/products/blue_chudi.jpg"),
                Product(name="White Nighty", category="Nightyila", fabric="Cotton", price=800, stock=15, image_path="/static/images/products/white_nighty.jpg"),
                Product(name="Embroidered Blouse", category="Blouse", fabric="searasa", price=1200, stock=8, image_path="/static/images/products/embroidered_blouse.jpg")
            ])
            db.session.commit()
    app.run(debug=True)