from django.http import JsonResponse
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
import boto3

dynamodb = boto3.resource('dynamodb', 'eu-west-1')
table_name = 'x23211946_EphUsers'
table = dynamodb.Table(table_name)

def access_token_required(func):
    def wrapper(request, *args, **kwargs):
        id_value = request.headers.get('id')
        access_token = request.headers.get('Access-Token')

        print(id_value, access_token)
        
        if not id_value or not access_token:
            return JsonResponse({'error': 'Missing id or Access-Token headers'}, status=400)
        
        filter_expression = Attr('id').eq(id_value)
        
        try:
            response = table.scan(FilterExpression=filter_expression)
            item = response['Items'][0]
        except ClientError as e:
            print(e.response['Error']['Message'])
            return JsonResponse({'error': 'Failed to retrieve data from DynamoDB'}, status=500)
        
        if not item:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        if access_token != item.get('access_token'):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        return func(request, *args, **kwargs)
    return wrapper
