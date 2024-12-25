from jinja2 import Template
from typing import Optional

# Simulate a simple in-memory database for storing mock API configurations
mock_apis = {}

def create_mock_api(api_name: str, method: str, response_template: str):
    """Create a new mock API with a given template."""
    if api_name in mock_apis:
        raise Exception("API already exists.")
    
    # Store API details (method and template) for future use
    mock_apis[api_name] = {
        "method": method,
        "response_template": response_template
    }

def get_mock_api_response(api_name: str, user_id: Optional[int] = None, name: Optional[str] = None, activity: Optional[str] = None):
    """Generate a dynamic response based on the stored template."""
    if api_name not in mock_apis:
        raise Exception("API not found.")
    
    # Get the response template from the mock API configuration
    api = mock_apis[api_name]
    template = Template(api["response_template"])
    
    # Render the template with query parameters
    response = template.render(user_id=user_id, name=name, activity=activity)
    
    return response
