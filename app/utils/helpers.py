"""Helper utility functions"""

def validate_input(data, required_fields):
    """
    Validate that required fields are present in data
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
        
    Returns:
        tuple: (is_valid, missing_fields)
    """
    missing = [field for field in required_fields if field not in data or data[field] is None]
    return (len(missing) == 0, missing)

