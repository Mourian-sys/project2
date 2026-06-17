"""
User model for database
"""

from datetime import datetime


class User:
    """
    User model representing an application user
    """
    
    def __init__(self, username, email, password_hash):
        self.id = None
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.is_active = True
        self.is_admin = False
    
    def to_dict(self):
        """
        Convert user to dictionary
        
        Returns:
            dict: User data
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active,
            'is_admin': self.is_admin
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
