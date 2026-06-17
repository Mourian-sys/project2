"""
API routes
"""

from flask import Blueprint, request, jsonify
from utils.logger import get_logger
from utils.helpers import format_response, validate_input
from utils.decorators import validate_json_request, handle_errors, log_request
from services.data_service import DataService

logger = get_logger(__name__)
api_bp = Blueprint('api', __name__)


@api_bp.route('/process', methods=['POST'])
@validate_json_request
@handle_errors
@log_request
def process():
    """
    Process data endpoint
    """
    data = request.get_json()
    
    # Validate input
    if 'items' not in data:
        raise KeyError('items')
    
    items = data.get('items')
    
    # Validate items
    is_valid, error = validate_input(items, input_type=list, min_length=1)
    if not is_valid:
        raise ValueError(error)
    
    # Process items
    result = DataService.process_items(items)
    
    if result['success']:
        logger.info(f'Successfully processed {result["input_count"]} items')
        return jsonify(format_response(result)), 200
    else:
        logger.error(f'Error processing items: {result["error"]}')
        return jsonify(format_response(
            result,
            status='error',
            code=400
        )), 400


@api_bp.route('/validate', methods=['POST'])
@validate_json_request
@handle_errors
@log_request
def validate():
    """
    Validate input endpoint
    """
    data = request.get_json()
    
    if 'value' not in data:
        raise KeyError('value')
    
    value = data.get('value')
    is_valid, error = validate_input(value)
    
    if is_valid:
        return jsonify(format_response({
            'valid': True,
            'value': value
        })), 200
    else:
        return jsonify(format_response(
            {'valid': False, 'error': error},
            status='error',
            code=400
        )), 400


@api_bp.route('/aggregate', methods=['POST'])
@validate_json_request
@handle_errors
@log_request
def aggregate():
    """
    Aggregate data endpoint
    """
    data = request.get_json()
    
    if 'data' not in data:
        raise KeyError('data')
    
    data_items = data.get('data')
    aggregation_type = data.get('type', 'count')
    
    try:
        result = DataService.aggregate_data(data_items, aggregation_type)
        return jsonify(format_response(result)), 200
    except ValueError as e:
        return jsonify(format_response(
            {'error': str(e)},
            status='error',
            code=400
        )), 400


@api_bp.route('/filter', methods=['POST'])
@validate_json_request
@handle_errors
@log_request
def filter_data():
    """
    Filter data endpoint
    """
    data = request.get_json()
    
    if 'items' not in data:
        raise KeyError('items')
    
    items = data.get('items')
    filter_type = data.get('filter', 'non_empty')
    
    # Define filter functions
    filters = {
        'non_empty': lambda x: x and str(x).strip(),
        'numeric': lambda x: isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.', '').isdigit()),
        'string': lambda x: isinstance(x, str),
        'length_gt_5': lambda x: isinstance(x, str) and len(x) > 5
    }
    
    filter_func = filters.get(filter_type)
    if not filter_func:
        raise ValueError(f'Unknown filter type: {filter_type}')
    
    try:
        filtered = DataService.filter_items(items, filter_func)
        return jsonify(format_response({
            'input_count': len(items),
            'output_count': len(filtered),
            'filter_type': filter_type,
            'results': filtered
        })), 200
    except Exception as e:
        return jsonify(format_response(
            {'error': str(e)},
            status='error',
            code=400
        )), 400


@api_bp.route('/echo', methods=['POST'])
@validate_json_request
@handle_errors
@log_request
def echo():
    """
    Echo endpoint - returns received data
    """
    data = request.get_json()
    logger.info('Echo endpoint called')
    return jsonify(format_response({
        'echo': data,
        'timestamp': str(__import__('datetime').datetime.utcnow())
    })), 200
