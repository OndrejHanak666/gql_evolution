from datetime import datetime

def parse_datetime(value):
    """Parse a datetime string into a datetime object."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        # Handle ISO format datetime strings
        try:
            return datetime.fromisoformat(value.replace('T', ' '))
        except ValueError:
            # If the above fails, try parsing with explicit format
            try:
                return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                try:
                    return datetime.strptime(value, '%Y-%m-%d')
                except ValueError:
                    raise ValueError(f"Cannot parse datetime from {value}")
    raise ValueError(f"Cannot parse datetime from {value} of type {type(value)}")

def process_model_dates(data, date_fields=None):
    """Process a dictionary of model data to convert datetime strings to datetime objects.
    
    Args:
        data (dict): The model data dictionary
        date_fields (list): Optional list of field names that should be treated as dates
                          In addition to 'created' and 'lastchange'
    """
    if date_fields is None:
        date_fields = []
    
    # Always include the base model datetime fields
    date_fields.extend(['created', 'lastchange'])
    
    # Create a new dict to avoid modifying the input
    processed = data.copy()
    
    # Convert all datetime fields
    for field in date_fields:
        if field in processed and processed[field] is not None:
            processed[field] = parse_datetime(processed[field])
            
    return processed

def process_json_data(data):
    """Process JSON data to convert datetime strings to datetime objects."""
    processed = {}
    
    # Define which fields should be treated as dates for each model
    date_fields_map = {
        'publications': ['published_date'],
        'events': ['startdate', 'enddate']  # Add other date fields for other models here
    }
    
    for model_name, items in data.items():
        processed[model_name] = []
        date_fields = date_fields_map.get(model_name, [])
        
        for item in items:
            processed_item = process_model_dates(item, date_fields)
            processed[model_name].append(processed_item)
    
    return processed