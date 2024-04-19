import boto3
from boto3.dynamodb.conditions import Attr, Key
from S3.displayPic import DisplayPic
import uuid
import secrets
import time

dyn_resource = boto3.resource('dynamodb', 'eu-west-1')

class Users:

    def __init__(self):
        self.dyn_resource = dyn_resource
        self.table = None

    def create_table(self):
        try:
            self.table = self.dyn_resource.create_table(
                TableName='x23211946_EphUsers',
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'}, 
                    {'AttributeName': 'eph_id', 'KeyType': 'RANGE'} 
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'eph_id', 'AttributeType': 'S'},
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                },
                GlobalSecondaryIndexes=[  
                    {
                        'IndexName': 'EphIdIndex',
                        'KeySchema': [
                            {'AttributeName': 'eph_id', 'KeyType': 'HASH'} 
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'  
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 1,
                            'WriteCapacityUnits': 1
                        }
                    }
                ]
            )
            response = {'successful': True, 'message': 'Creation successful'}
        except Exception as e:
            response = {'successful': False, 'message': str(e)}
            
        return response

        
    def auth_user(self, eph_id, password):
        table_name = 'x23211946_EphUsers'
        table = self.dyn_resource.Table(table_name)
    
        try:
            response = table.query(
                IndexName='EphIdIndex',  
                KeyConditionExpression=Key('eph_id').eq('#'+eph_id)
            )
            if response['Items']: 
                obj = response['Items'][0]  
                eph_password = obj['password']
                if password == eph_password:
                    pic_instance = DisplayPic()
                    pic_request = pic_instance.get_presigned_url(obj['eph_id'][1:])
                    if pic_request['successful']:
                        response = {'successful': True, 'message': {
                            'access_token': obj['access_token'], 'id': obj['id'], 'eph_id': obj['eph_id'],
                            'first_name': obj['first_name'], 'last_name': obj['last_name'],
                            'email': obj['email'], 'display_pic': pic_request["message"]}}
                else:
                    response = {'successful': False, 'message': 'Authentication Failed'}
            else:
                response = {'successful': False, 'message': 'User not found'}
    
        except Exception as e:
            response = {'successful': False, 'message': str(e)}
    
        return response

    
    def create_user(self, first_name, last_name, email, password):
        table_name = 'x23211946_EphUsers'
        table = self.dyn_resource.Table(table_name)
        id_value = str(uuid.uuid4())
        
        hex_value = hex(int(time.time()))[2:]  
        eph_id = '#EP' + hex_value[-3:]  
    
        access_token = secrets.token_hex(20)
    
        item = {
            'id': id_value,
            'eph_id': eph_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'access_token': access_token
        }
        
        response = table.put_item(Item=item)
        
        response2 = {"id": id_value, "eph_id": eph_id, "access_token": access_token, "response": response}
    
        return response2
        
    def get_user(self, eph_id):
        table_name = 'x23211946_EphUsers'
        table = self.dyn_resource.Table(table_name)
    
        try:
            response = table.query(
                IndexName='EphIdIndex',  
                KeyConditionExpression=Key('eph_id').eq('#'+eph_id)
            )
            if response['Items']: 
                item = response['Items'][0]
                pic_instance = DisplayPic()
                pic_request = pic_instance.get_presigned_url(eph_id)
                if pic_request['successful']:
                    item['display_pic'] = pic_request['message']
                    return {'successful': True, 'item': item}
                else:
                    return {'successful': True, 'item': item}
            else:
                return {'successful': False, 'message': 'No item found for eph_id: {}'.format(eph_id)}
        except Exception as e:
            return {'successful': False, 'message': str(e)}



    
        
