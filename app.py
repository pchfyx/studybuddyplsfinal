from flask import Flask
from flask_login import LoginManager
from models import db, User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a random secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_buddy.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Import and register blueprints
    from routes import main, auth, groups
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(groups)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)