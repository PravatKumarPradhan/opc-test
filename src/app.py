from flask import Flask
from src.routes import bp
from database import init_db

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    init_db()
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
