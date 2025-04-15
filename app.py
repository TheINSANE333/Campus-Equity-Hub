from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import current_user
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import timedelta
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from wtforms import PasswordField
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=30)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Create Admin decorator for protected routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        
        # Get the user from database
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    token = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    campus = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Custom model view that handles password changes properly
class SecureUserModelView(ModelView):
    form_base_class = SecureForm
    column_exclude_list = ['password']
    form_excluded_columns = ['password']
    column_searchable_list = ['username', 'email']
    column_filters = ['is_admin']
    
    # Add custom password field
    form_extra_fields = {
        'new_password': PasswordField('New Password')
    }
    
    def on_model_change(self, form, model, is_created):
        # If new password is provided, hash it
        if form.new_password.data:
            model.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
    
    def is_accessible(self):
        if 'user_id' not in session:
            return False
        
        user = User.query.get(session['user_id'])
        return user is not None and user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('index'))

# Assuming we have a Campus model - add this to your models section
class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Campus {self.name}>'
    
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    read = db.Column(db.Boolean, default=False)
    
    # Define relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    
    def __repr__(self):
        return f'<Chat {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'sender_username': self.sender.username,
            'receiver_username': self.receiver.username,
            'message': self.message,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'read': self.read
        }

# Create an initial admin user after database initialization
# Initialize Flask-Admin
admin = Admin(app, name='Admin Dashboard', template_mode='bootstrap4')

# Add ModelView
admin.add_view(SecureUserModelView(User, db.session))

def create_admin_user():
    with app.app_context():
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Create admin user
            admin_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(username='admin', email='admin@example.com', password=admin_password, token='0', is_admin=True, campus='MMU')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

# Create an initial user after database initialization
def create_user1():
    with app.app_context():
        # Check if admin user already exists
        user1 = User.query.filter_by(username='user1').first()
        if not user1:
            # Create user1
            admin_password = bcrypt.generate_password_hash('user1123').decode('utf-8')
            user_1 = User(username='user1', email='user@example.com', password=admin_password, token='0', is_admin=False, campus='MMU')
            db.session.add(user_1)
            db.session.commit()
            print("User1 created.")
        else:
            print("User1 already exists.")

# Sample data insertion function - you can use this to populate your database with sample data
def create_sample_campuses():
    with app.app_context():
        # Check if campuses already exist
        if Campus.query.count() == 0:
            campuses = [
                Campus(name='Multimedia University', location='Cyberjaya', description=''),
                Campus(name='Multimedia University', location='Melaka', description=''),
                Campus(name='University Malaya', location='Kuala Lumpur', description=''),
                Campus(name='Sunway Univerisity', location='Subang Jaya', description=''),
                Campus(name='Monash University', location='Subang Jaya', description=''),
                Campus(name='Taylors University', location='Subang Jaya', description=''),
                Campus(name='Universiti Sains Malaysia', location='Penang', description=''),
                Campus(name='Tunku Abdul Rahman University of Management and Technology', location='Kuala Lumpur', description=''),
                Campus(name='Universiti Tunku Abdul Rahman', location='Kampar', description=''),
                Campus(name='Universiti Tunku Abdul Rahman', location='Kuala Lumpur', description=''),
                Campus(name='Asia Pacific University', location='Kuala Lumpur', description=''),
            ]
            
            db.session.add_all(campuses)
            db.session.commit()
            print("Sample campuses created.")

# Create database tables
with app.app_context():
    db.create_all()
    create_admin_user()
    create_user1()
    create_sample_campuses()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        campus = request.form['campus']
        
        # Check if username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        
        if existing_user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('signup'))
        
        if existing_email:
            flash('Email already registered!', 'danger')
            return redirect(url_for('signup'))
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create new user
        new_user = User(username=username, email=email, password=hashed_password, campus=campus, token=0)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Add route for campus search API endpoint
@app.route('/api/campus-search')
def campus_search_api():
    query = request.args.get('query', '')
    
    if query:
        # Search for campuses that match the query (case-insensitive)
        campuses = Campus.query.filter(
            db.or_(
                Campus.name.ilike(f'%{query}%'),
                Campus.location.ilike(f'%{query}%')
            )
        ).limit(10).all()
        
        # Format results for JSON response
        results = [
            {
                'id': campus.id,
                'name': campus.name,
                'location': campus.location,
                'text': f"{campus.name} - {campus.location}"
            }
            for campus in campuses
        ]
    else:
        # Return empty results if no query provided
        results = []
    
    return jsonify(results)

# Add route to get campus details
@app.route('/api/campus/<int:campus_id>')
def campus_details(campus_id):
    campus = Campus.query.get_or_404(campus_id)
    return jsonify({
        'id': campus.id,
        'name': campus.name,
        'location': campus.location,
        'description': campus.description
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and bcrypt.check_password_hash(user.password, password):
            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            session['campus'] = user.campus
            session['token'] = user.token

            flash(f'Welcome back, {user.username}!', 'success')

            # Redirect admin users to admin dashboard
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    
    return render_template('login.html')

# Add an admin dashboard route
@app.route('/admin-dashboard')
@admin_required
def admin_dashboard():
    # Get all users
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

# Add a route to reset database
@app.route('/reset-database', methods=['GET', 'POST'])
@admin_required  # Only admins can access this function
def reset_database():
    if request.method == 'POST':
        if request.form.get('confirm') == 'RESET':
            with app.app_context():
                # Drop all tables
                db.drop_all()
                
                # Recreate all tables
                db.create_all()
                
                # Recreate the admin user
                create_admin_user()

                # Recreate the user1
                create_user1()

                # Recreate the campus
                create_sample_campuses()
                
                # Clear the session
                session.clear()
                
                flash('Database has been reset successfully. Please log in again.', 'success')
                return redirect(url_for('login'))
        else:
            flash('Confirmation text did not match. Database was not reset.', 'danger')
            
    return render_template('reset_database.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        session.pop('username', None)
        flash('You have been logged out.', 'info')
    
    return redirect(url_for('index'))

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        flash('Please log in to access the chat.', 'danger')
        return redirect(url_for('login'))
        
    # Get all users except the current user
    users = User.query.filter(User.id != session['user_id']).all()
    
    # Get unread message counts for navbar indicator
    unread_counts = db.session.query(
        Chat.sender_id, 
        db.func.count(Chat.id).label('count')
    ).filter(
        Chat.receiver_id == session['user_id'],
        Chat.read == False
    ).group_by(Chat.sender_id).all()
    
    unread_by_user = {sender_id: count for sender_id, count in unread_counts}
    
    return render_template('chat.html', users=users, unread_by_user=unread_by_user)

@app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
def chat_with_user(user_id):
    if 'user_id' not in session:
        flash('Please log in to access the chat.', 'danger')
        return redirect(url_for('login'))
    
    current_user_id = session['user_id']
    
    # Check if the user exists
    chat_partner = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        message = request.form.get('message')
        
        if message:
            # Create new chat message
            new_message = Chat(
                sender_id=current_user_id,
                receiver_id=user_id,
                message=message
            )
            
            db.session.add(new_message)
            db.session.commit()
            
            # If AJAX request, return the new message as JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(new_message.to_dict())
        
        # For normal form submission, redirect back to the chat
        return redirect(url_for('chat_with_user', user_id=user_id))
    
    # Mark messages as read
    unread_messages = Chat.query.filter_by(
        sender_id=user_id,
        receiver_id=current_user_id,
        read=False
    ).all()
    
    for msg in unread_messages:
        msg.read = True
    
    db.session.commit()
    
    # Get all messages between the current user and the selected user
    messages = Chat.query.filter(
        ((Chat.sender_id == current_user_id) & (Chat.receiver_id == user_id)) |
        ((Chat.sender_id == user_id) & (Chat.receiver_id == current_user_id))
    ).order_by(Chat.timestamp).all()
    
    # Get all users except the current user for the sidebar
    users = User.query.filter(User.id != current_user_id).all()
    
    # Get unread message counts
    unread_counts = db.session.query(
        Chat.sender_id, 
        db.func.count(Chat.id).label('count')
    ).filter(
        Chat.receiver_id == current_user_id,
        Chat.read == False
    ).group_by(Chat.sender_id).all()
    
    unread_by_user = {sender_id: count for sender_id, count in unread_counts}
    
    return render_template(
        'chat_with_user.html',
        chat_partner=chat_partner,
        messages=messages,
        users=users,
        unread_by_user=unread_by_user
    )

@app.route('/api/messages/<int:user_id>')
def get_new_messages(user_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    current_user_id = session['user_id']
    last_id = request.args.get('last_id', 0, type=int)
    
    # Get new messages that the current user hasn't seen yet
    new_messages = Chat.query.filter(
        Chat.id > last_id,
        ((Chat.sender_id == current_user_id) & (Chat.receiver_id == user_id)) |
        ((Chat.sender_id == user_id) & (Chat.receiver_id == current_user_id))
    ).order_by(Chat.timestamp).all()
    
    # Mark messages as read
    unread_messages = [msg for msg in new_messages if msg.receiver_id == current_user_id and not msg.read]
    for msg in unread_messages:
        msg.read = True
    
    db.session.commit()
    
    return jsonify([message.to_dict() for message in new_messages])

@app.route('/api/unread-counts')
def get_unread_counts():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    current_user_id = session['user_id']
    
    # Get unread message counts
    unread_counts = db.session.query(
        Chat.sender_id, 
        db.func.count(Chat.id).label('count')
    ).filter(
        Chat.receiver_id == current_user_id,
        Chat.read == False
    ).group_by(Chat.sender_id).all()
    
    unread_by_user = {str(sender_id): count for sender_id, count in unread_counts}
    total_unread = sum(unread_by_user.values())
    
    return jsonify({
        'by_user': unread_by_user,
        'total': total_unread
    })

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)