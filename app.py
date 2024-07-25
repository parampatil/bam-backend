from flask import Flask
from flask_cors import CORS
from config import Config
from routes import register_blueprints

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Register Blueprints
register_blueprints(app)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
