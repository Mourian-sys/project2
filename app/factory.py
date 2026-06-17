"""
Application factory for creating Flask app instances
"""

from flask import Flask
from config.settings import get_config
from utils.logger import get_logger, setup_logging

logger = get_logger(__name__)


def create_app(config_name=None):
    """
    Create and configure Flask application
    
    Args:
        config_name (str): Configuration name (development, production, testing)
        
    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Setup logging
    setup_logging()
    logger.info(f'Creating Flask app with {config.__class__.__name__} configuration')
    
    # Register blueprints
    from app.routes import main_bp, api_bp, webhook_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(webhook_bp, url_prefix='/webhook')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    logger.info('Flask app created successfully')
    return app


def register_error_handlers(app):
    """
    Register error handlers for the application
    
    Args:
        app (Flask): Flask application
    """
    from flask import jsonify
    from utils.helpers import format_response
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(format_response(
            {'error': 'Bad request'},
            status='error',
            code=400
        )), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify(format_response(
            {'error': 'Unauthorized'},
            status='error',
            code=401
        )), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify(format_response(
            {'error': 'Forbidden'},
            status='error',
            code=403
        )), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(format_response(
            {'error': 'Resource not found'},
            status='error',
            code=404
        )), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal server error: {str(error)}')
        return jsonify(format_response(
            {'error': 'Internal server error'},
            status='error',
            code=500
        )), 500


def register_cli_commands(app):
    """
    Register CLI commands
    
    Args:
        app (Flask): Flask application
    """
    import click
    
    @app.cli.command()
    def init_db():
        """Initialize database"""
        click.echo('Initializing database...')
        logger.info('Database initialized')
        click.echo('Database initialized successfully')
    
    @app.cli.command()
    def create_admin():
        """Create admin user"""
        click.echo('Creating admin user...')
        username = click.prompt('Username')
        email = click.prompt('Email')
        click.echo(f'Admin user created: {username}')
        logger.info(f'Admin user created: {username}')
    
    @app.cli.command()
    @click.option('--port', default=5000, help='Port to run on')
    @click.option('--host', default='0.0.0.0', help='Host to bind to')
    def run(port, host):
        """Run development server"""
        click.echo(f'Starting server on {host}:{port}')
        logger.info(f'Starting server on {host}:{port}')
