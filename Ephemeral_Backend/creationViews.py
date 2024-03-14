from django.http import JsonResponse
from .dynoDb import Users
import json

def create_user(request):
    if request.method == 'POST':
        raw_data = request.body
        try:
            body_data = json.loads(raw_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        first_name = body_data.get('first_name')
        last_name = body_data.get('last_name')
        email = body_data.get('email')
        password = body_data.get('password')
        
        user_instance = Users()
        response = user_instance.create_user(first_name, last_name, email, password)
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
          return JsonResponse({'successful': True, 'response': response})
        else:
          return JsonResponse({'successful': False, 'response': response})

    else:
        return JsonResponse({'successful': False, 'response': {'error': 'Unsupported HTTP method', 'status': 405}})
    
def test_body(request):
    if request.method == 'POST':
        raw_data = request.body
        try:
            body_data = json.loads(raw_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        name = body_data.get('id')
        return JsonResponse({'message': f'Hello, {name}!'})

    else:
        # Return an error response for unsupported HTTP methods
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)