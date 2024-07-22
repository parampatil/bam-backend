# routes/__init__.py
from .auth_routes import auth_bp
from .user_routes import user_bp
from .paper_routes import paper_bp
from .collection_routes import collection_bp
from .author_routes import author_bp

# Optionally, you can add a function to register all blueprints
def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(paper_bp)
    app.register_blueprint(collection_bp)
    app.register_blueprint(author_bp)
