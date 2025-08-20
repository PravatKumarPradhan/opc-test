from flask import Flask
from src.database import init_db
from src.routes import bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"  # Needed for flash messages

    # Initialize database
    init_db()

    # Register blueprints
    app.register_blueprint(bp)

    return app

# Expose app globally so run.py can import it
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
