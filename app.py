from flask import Flask
from flask_cors import CORS
from config import Config
from routes import register_blueprints

from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Swagger UI
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    app.config['SWAGGER_URL'],  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    app.config['API_URL'],
    config={  # Swagger UI config overrides
        'app_name': "BAM API",
    },
)

app.register_blueprint(swaggerui_blueprint)

# Register Blueprints
register_blueprints(app)

@app.route('/')
def hello_world():
    return 'Welcome to Building A Mind API!'

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
