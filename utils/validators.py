"""
Validation functions for various data types
"""

import re
import json
from urllib.parse import urlparse


def validate_email(email):
    """
    Validate email address format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_url(url):
    """
    Validate URL format
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(url, str):
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_json(json_str):
    """
    Validate JSON format
    
    Args:
        json_str (str): JSON string to validate
        
    Returns:
        tuple: (is_valid, parsed_data or error_message)
    """
    if not isinstance(json_str, str):
        return False, 'Input must be a string'
    
    try:
        data = json.loads(json_str)
        return True, data
    except json.JSONDecodeError as e:
        return False, f'Invalid JSON: {str(e)}'


def validate_phone(phone):
    """
    Validate phone number format
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(phone, str):
        return False
    
    # Remove common separators
    cleaned = re.sub(r'[\s().-]', '', phone)
    
    # Check if it contains only digits and has reasonable length
    return cleaned.isdigit() and 10 <= len(cleaned) <= 15


def validate_password(password, min_length=8, require_uppercase=True, 
                     require_numbers=True, require_special=True):
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
        min_length (int): Minimum password length
        require_uppercase (bool): Require uppercase letters
        require_numbers (bool): Require numbers
        require_special (bool): Require special characters
        
    Returns:
        tuple: (is_valid, error_message or None)
    """
    if not isinstance(password, str):
        return False, 'Password must be a string'
    
    if len(password) < min_length:
        return False, f'Password must be at least {min_length} characters'
    
    if require_uppercase and not any(c.isupper() for c in password):
        return False, 'Password must contain uppercase letters'
    
    if require_numbers and not any(c.isdigit() for c in password):
        return False, 'Password must contain numbers'
    
    if require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, 'Password must contain special characters'
    
    return True, None


def validate_ip_address(ip):
    """
    Validate IPv4 address format
    
    Args:
        ip (str): IP address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(ip, str):
        return False
    
    pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(pattern, ip) is not None


def validate_credit_card(card_number):
    """
    Validate credit card number using Luhn algorithm
    
    Args:
        card_number (str): Credit card number
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(card_number, str):
        return False
    
    # Remove spaces and dashes
    digits = card_number.replace(' ', '').replace('-', '')
    
    if not digits.isdigit() or len(digits) < 13:
        return False
    
    # Luhn algorithm
    total = 0
    for i, digit in enumerate(reversed(digits)):
        d = int(digit)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    
    return total % 10 == 0
