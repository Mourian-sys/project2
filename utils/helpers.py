"""
Helper functions for the application
"""

import re
import json
from functools import wraps
from utils.logger import get_logger

logger = get_logger(__name__)


def format_response(data=None, status='success', code=200, message=None):
    """
    Format API response in standard format
    
    Args:
        data (dict): Response data
        status (str): Status message (success/error/warning)
        code (int): HTTP status code
        message (str): Additional message
        
    Returns:
        dict: Formatted response
    """
    response = {
        'status': status,
        'code': code,
    }
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    return response


def validate_input(value, input_type=str, min_length=1, max_length=None, 
                   required=True, pattern=None):
    """
    Validate input value with multiple criteria
    
    Args:
        value: Value to validate
        input_type: Expected type
        min_length: Minimum length (for strings/lists)
        max_length: Maximum length (for strings/lists)
        required: Whether value is required
        pattern: Regex pattern for string validation
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check if required
    if not required and value is None:
        return True, None
    
    if value is None:
        return False, 'Value cannot be None'
    
    # Check type
    if not isinstance(value, input_type):
        return False, f'Value must be of type {input_type.__name__}'
    
    # Check length for strings/lists
    if isinstance(value, (str, list)):
        if len(value) < min_length:
            return False, f'Value must be at least {min_length} characters/items'
        if max_length and len(value) > max_length:
            return False, f'Value must be at most {max_length} characters/items'
    
    # Check pattern for strings
    if isinstance(value, str) and pattern:
        if not re.match(pattern, value):
            return False, f'Value does not match required pattern: {pattern}'
    
    return True, None


def sanitize_input(value, max_length=1000):
    """
    Sanitize input to prevent injection attacks
    
    Args:
        value: Input value to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized input
    """
    if not isinstance(value, str):
        value = str(value)
    
    # Remove control characters
    value = ''.join(char for char in value if ord(char) >= 32 or char in '\n\t')
    
    # Limit length
    if len(value) > max_length:
        value = value[:max_length]
    
    return value.strip()


def process_data(items, transform_func=None):
    """
    Process a list of items with optional transformation
    
    Args:
        items (list): List of items to process
        transform_func: Function to apply to each item
        
    Returns:
        list: Processed items
    """
    if not isinstance(items, list):
        raise TypeError('Items must be a list')
    
    logger.info(f'Processing {len(items)} items')
    
    if transform_func is None:
        transform_func = lambda x: str(x).upper()
    
    try:
        processed = [transform_func(item) for item in items]
        logger.info(f'Successfully processed {len(processed)} items')
        return processed
    except Exception as e:
        logger.error(f'Error processing items: {str(e)}')
        raise


def handle_exceptions(func):
    """
    Decorator to handle exceptions in functions
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Error in {func.__name__}: {str(e)}')
            raise
    return wrapper


def retry(max_attempts=3, delay=1):
    """
    Decorator to retry function execution
    
    Args:
        max_attempts (int): Maximum number of attempts
        delay (int): Delay between attempts in seconds
        
    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_attempts - 1:
                        logger.warning(f'Attempt {attempt + 1} failed, retrying in {delay}s...')
                        time.sleep(delay)
                    else:
                        logger.error(f'All {max_attempts} attempts failed')
                        raise
        return wrapper
    return decorator


def parse_json_safely(json_str, default=None):
    """
    Safely parse JSON string
    
    Args:
        json_str (str): JSON string to parse
        default: Default value if parsing fails
        
    Returns:
        dict: Parsed JSON or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f'Error parsing JSON: {str(e)}')
        return default
