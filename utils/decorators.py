"""
Decorators for common functionality
"""

from functools import wraps
from flask import request, jsonify
from utils.logger import get_logger
from utils.helpers import format_response

logger = get_logger(__name__)


def require_auth(f):
    """
    Decorator to require authentication
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning('Missing Authorization header')
            return jsonify(format_response(
                {'error': 'Missing Authorization header'},
                status='error',
                code=401
            )), 401
        
        # Simple Bearer token validation
        if not auth_header.startswith('Bearer '):
            logger.warning('Invalid Authorization header format')
            return jsonify(format_response(
                {'error': 'Invalid Authorization header format'},
                status='error',
                code=401
            )), 401
        
        token = auth_header.split(' ')[1]
        if not token:
            logger.warning('Missing token')
            return jsonify(format_response(
                {'error': 'Missing token'},
                status='error',
                code=401
            )), 401
        
        return f(*args, **kwargs)
    return decorated_function


def validate_json_request(f):
    """
    Decorator to validate JSON request body
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            logger.warning('Request is not JSON')
            return jsonify(format_response(
                {'error': 'Request must be JSON'},
                status='error',
                code=400
            )), 400
        
        try:
            data = request.get_json()
            if data is None:
                logger.warning('Empty JSON body')
                return jsonify(format_response(
                    {'error': 'Empty JSON body'},
                    status='error',
                    code=400
                )), 400
        except Exception as e:
            logger.error(f'Error parsing JSON: {str(e)}')
            return jsonify(format_response(
                {'error': f'Invalid JSON: {str(e)}'},
                status='error',
                code=400
            )), 400
        
        return f(*args, **kwargs)
    return decorated_function


def rate_limit(max_requests=100, window=3600):
    """
    Decorator for rate limiting (basic in-memory implementation)
    
    Args:
        max_requests (int): Maximum requests allowed
        window (int): Time window in seconds
        
    Returns:
        Decorated function
    """
    def decorator(f):
        requests_log = {}
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            import time
            
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Clean old entries
            requests_log[client_ip] = [
                req_time for req_time in requests_log.get(client_ip, [])
                if current_time - req_time < window
            ]
            
            # Check limit
            if len(requests_log.get(client_ip, [])) >= max_requests:
                logger.warning(f'Rate limit exceeded for {client_ip}')
                return jsonify(format_response(
                    {'error': 'Rate limit exceeded'},
                    status='error',
                    code=429
                )), 429
            
            # Add current request
            if client_ip not in requests_log:
                requests_log[client_ip] = []
            requests_log[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def handle_errors(f):
    """
    Decorator to handle errors in API endpoints
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.error(f'ValueError: {str(e)}')
            return jsonify(format_response(
                {'error': str(e)},
                status='error',
                code=400
            )), 400
        except KeyError as e:
            logger.error(f'KeyError: {str(e)}')
            return jsonify(format_response(
                {'error': f'Missing field: {str(e)}'},
                status='error',
                code=400
            )), 400
        except Exception as e:
            logger.error(f'Unexpected error: {str(e)}')
            return jsonify(format_response(
                {'error': 'Internal server error'},
                status='error',
                code=500
            )), 500
    return decorated_function


def log_request(f):
    """
    Decorator to log API requests and responses
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.info(f'Request: {request.method} {request.path}')
        logger.debug(f'Headers: {dict(request.headers)}')
        
        try:
            result = f(*args, **kwargs)
            logger.info(f'Response: 200 OK')
            return result
        except Exception as e:
            logger.error(f'Request failed: {str(e)}')
            raise
    return decorated_function
