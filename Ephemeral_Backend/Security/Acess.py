from django.http import JsonResponse
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'x23211946_EphUsers'
table = dynamodb.Table(table_name)

def access_token_required(func):
    def wrapper(request, *args, **kwargs):
        id_value = request.headers.get('id')
        access_token = request.headers.get('Access-Token')
        
        if not id_value or not access_token:
            return JsonResponse({'error': 'Missing id or Access-Token headers'}, status=400)
        
        response = table.get_item(Key={'id': id_value})
        item = response.get('Item')
        
        if not item:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        if access_token != item.get('access_token'):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        return func(request, *args, **kwargs)
    return wrapper
