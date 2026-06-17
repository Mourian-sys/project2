"""
Webhook handling service
"""

import json
import hmac
import hashlib
from utils.logger import get_logger

logger = get_logger(__name__)


class WebhookService:
    """
    Service for handling webhooks from external services
    """
    
    @staticmethod
    def verify_github_signature(payload, signature, secret):
        """
        Verify GitHub webhook signature
        
        Args:
            payload (bytes): Raw request body
            signature (str): X-Hub-Signature header value
            secret (str): Webhook secret
            
        Returns:
            bool: True if signature is valid
        """
        if not secret:
            logger.warning('No webhook secret configured')
            return False
        
        try:
            # Compute expected signature
            expected_signature = 'sha256=' + hmac.new(
                secret.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures
            is_valid = hmac.compare_digest(signature, expected_signature)
            
            if is_valid:
                logger.info('GitHub webhook signature verified')
            else:
                logger.warning('GitHub webhook signature verification failed')
            
            return is_valid
        except Exception as e:
            logger.error(f'Error verifying webhook signature: {str(e)}')
            return False
    
    @staticmethod
    def parse_github_payload(payload):
        """
        Parse GitHub webhook payload
        
        Args:
            payload (dict): Webhook payload
            
        Returns:
            dict: Parsed webhook data
        """
        try:
            return {
                'event_type': 'github',
                'repository': payload.get('repository', {}).get('full_name'),
                'branch': payload.get('ref', '').split('/')[-1],
                'commits': len(payload.get('commits', [])),
                'pusher': payload.get('pusher', {}).get('name'),
                'timestamp': payload.get('timestamp')
            }
        except Exception as e:
            logger.error(f'Error parsing GitHub payload: {str(e)}')
            return None
    
    @staticmethod
    def trigger_deployment(webhook_data):
        """
        Trigger deployment based on webhook data
        
        Args:
            webhook_data (dict): Webhook data
            
        Returns:
            dict: Deployment result
        """
        try:
            logger.info(f'Triggering deployment for {webhook_data.get("repository")}')
            
            # Here you would integrate with Jenkins or other deployment service
            # For now, just log the request
            
            return {
                'success': True,
                'message': 'Deployment triggered',
                'repository': webhook_data.get('repository'),
                'branch': webhook_data.get('branch')
            }
        except Exception as e:
            logger.error(f'Error triggering deployment: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }
