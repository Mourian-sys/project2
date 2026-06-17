"""
Task model for database
"""

from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class Task:
    """
    Task model representing a background job
    """
    
    def __init__(self, title, description, user_id):
        self.id = None
        self.title = title
        self.description = description
        self.user_id = user_id
        self.status = TaskStatus.PENDING.value
        self.progress = 0
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.completed_at = None
    
    def to_dict(self):
        """
        Convert task to dictionary
        
        Returns:
            dict: Task data
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user_id': self.user_id,
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def update_progress(self, progress):
        """
        Update task progress
        
        Args:
            progress (int): Progress percentage (0-100)
        """
        self.progress = max(0, min(100, progress))
        self.updated_at = datetime.utcnow()
    
    def mark_completed(self):
        """
        Mark task as completed
        """
        self.status = TaskStatus.COMPLETED.value
        self.progress = 100
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def mark_failed(self):
        """
        Mark task as failed
        """
        self.status = TaskStatus.FAILED.value
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<Task {self.title}>'
