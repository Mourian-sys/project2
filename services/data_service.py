"""
Data processing service
"""

from utils.logger import get_logger
from utils.helpers import process_data, validate_input

logger = get_logger(__name__)


class DataService:
    """
    Service for data processing operations
    """
    
    @staticmethod
    def process_items(items):
        """
        Process a list of items
        
        Args:
            items (list): Items to process
            
        Returns:
            dict: Processing results
        """
        logger.info(f'DataService: Processing {len(items)} items')
        
        try:
            # Validate input
            is_valid, error = validate_input(items, input_type=list, min_length=1)
            if not is_valid:
                raise ValueError(error)
            
            # Process items
            processed = process_data(items)
            
            return {
                'success': True,
                'input_count': len(items),
                'output_count': len(processed),
                'results': processed
            }
        except Exception as e:
            logger.error(f'Error processing items: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def filter_items(items, filter_func):
        """
        Filter items based on function
        
        Args:
            items (list): Items to filter
            filter_func: Filter function
            
        Returns:
            list: Filtered items
        """
        try:
            filtered = [item for item in items if filter_func(item)]
            logger.info(f'Filtered {len(items)} items to {len(filtered)} items')
            return filtered
        except Exception as e:
            logger.error(f'Error filtering items: {str(e)}')
            raise
    
    @staticmethod
    def aggregate_data(data, aggregation_type='count'):
        """
        Aggregate data
        
        Args:
            data (list): Data to aggregate
            aggregation_type (str): Type of aggregation (count, sum, avg, min, max)
            
        Returns:
            dict: Aggregation results
        """
        try:
            if aggregation_type == 'count':
                result = len(data)
            elif aggregation_type == 'sum':
                result = sum(data)
            elif aggregation_type == 'avg':
                result = sum(data) / len(data) if data else 0
            elif aggregation_type == 'min':
                result = min(data) if data else None
            elif aggregation_type == 'max':
                result = max(data) if data else None
            else:
                raise ValueError(f'Unknown aggregation type: {aggregation_type}')
            
            logger.info(f'Aggregated data with {aggregation_type}: {result}')
            return {
                'type': aggregation_type,
                'result': result
            }
        except Exception as e:
            logger.error(f'Error aggregating data: {str(e)}')
            raise
