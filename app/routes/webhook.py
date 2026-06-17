"""
Webhook routes
"""

from flask import Blueprint, request, jsonify
from utils.logger import get_logger
from utils.helpers import format_response
from utils.decorators import log_request, handle_errors
from services.webhook_service import WebhookService
from config.settings import get_config

logger = get_logger(__name__)
webhook_bp = Blueprint('webhook', __name__)
config = get_config()


@webhook_bp.route('/github', methods=['POST'])
@handle_errors
@log_request
def github_webhook():
    """
    GitHub webhook endpoint
    """
    try:
        # Get request data
        payload = request.get_json()
        signature = request.headers.get('X-Hub-Signature-256', '')
        event_type = request.headers.get('X-GitHub-Event', 'unknown')
        
        logger.info(f'Received GitHub webhook event: {event_type}')
        
        # Verify signature if secret is configured
        if config.GITHUB_WEBHOOK_SECRET:
            if not WebhookService.verify_github_signature(
                request.data,
                signature,
                config.GITHUB_WEBHOOK_SECRET
            ):
                logger.warning('Invalid GitHub webhook signature')
                return jsonify(format_response(
                    {'error': 'Invalid signature'},
                    status='error',
                    code=401
                )), 401
        
        # Parse webhook payload
        webhook_data = WebhookService.parse_github_payload(payload)
        
        if not webhook_data:
            return jsonify(format_response(
                {'error': 'Could not parse webhook'},
                status='error',
                code=400
            )), 400
        
        # Handle push events
        if event_type == 'push':
            logger.info(f'Processing push event: {webhook_data}')
            
            # Trigger deployment
            deployment_result = WebhookService.trigger_deployment(webhook_data)
            
            if deployment_result['success']:
                return jsonify(format_response({
                    'message': 'Webhook processed successfully',
                    'event': event_type,
                    'data': webhook_data
                })), 200
            else:
                return jsonify(format_response(
                    deployment_result,
                    status='error',
                    code=500
                )), 500
        
        # Handle pull request events
        elif event_type == 'pull_request':
            logger.info(f'Processing pull request event')
            return jsonify(format_response({
                'message': 'Pull request event received',
                'event': event_type
            })), 200
        
        # Handle other events
        else:
            logger.info(f'Received unhandled event: {event_type}')
            return jsonify(format_response({
                'message': 'Event received',
                'event': event_type
            })), 200
    
    except Exception as e:
        logger.error(f'Error processing webhook: {str(e)}')
        return jsonify(format_response(
            {'error': str(e)},
            status='error',
            code=500
        )), 500


@webhook_bp.route('/test', methods=['POST'])
@handle_errors
@log_request
def test_webhook():
    """
    Test webhook endpoint
    """
    logger.info('Test webhook received')
    return jsonify(format_response({
        'message': 'Test webhook received successfully'
    })), 200
