"""
Main routes
"""

from flask import Blueprint, jsonify
from utils.logger import get_logger
from utils.helpers import format_response
from utils.decorators import log_request

logger = get_logger(__name__)
main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
@log_request
def home():
    """
    Home route
    """
    logger.info('Home route accessed')
    return jsonify(format_response({
        'message': 'Welcome to Project 2',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'api': '/api',
            'webhook': '/webhook/github'
        }
    }))


@main_bp.route('/health', methods=['GET'])
@log_request
def health():
    """
    Health check endpoint
    """
    logger.info('Health check requested')
    return jsonify(format_response({
        'status': 'healthy',
        'service': 'project2',
        'version': '1.0.0'
    }))


@main_bp.route('/status', methods=['GET'])
@log_request
def status():
    """
    Detailed status endpoint
    """
    import psutil
    import os
    
    try:
        return jsonify(format_response({
            'service': 'project2',
            'status': 'running',
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'uptime': os.popen('uptime').read().strip()
        }))
    except Exception:
        return jsonify(format_response({
            'service': 'project2',
            'status': 'running'
        }))


@main_bp.route('/about', methods=['GET'])
@log_request
def about():
    """
    About endpoint
    """
    return jsonify(format_response({
        'name': 'Project 2',
        'version': '1.0.0',
        'description': 'A comprehensive Python project with Jenkins CI/CD integration',
        'author': 'Mourian-sys',
        'repository': 'https://github.com/Mourian-sys/project2'
    }))
