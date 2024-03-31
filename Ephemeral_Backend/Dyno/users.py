import boto3
from boto3.dynamodb.conditions import Attr, Key
from Ephemeral_Backend.S3.displayPic import DisplayPic
import uuid
import secrets

dyn_resource = boto3.resource('dynamodb', 'eu-west-1')

class Users:

    def __init__(self):
        self.dyn_resource = dyn_resource
        self.table = None

    def create_table(self):
        self.table = self.dyn_resource.create_table(
            TableName='x23211946_EphUsers',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'},      
                {'AttributeName': 'eph_id', 'KeyType': 'RANGE'}   
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'eph_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        
    def auth_user(self, eph_id, password):
        table_name = 'x23211946_EphUsers'
        table = self.dyn_resource.Table(table_name)
        
        filter_expression = Attr('eph_id').eq('#' + eph_id)
        
        try:
           response = table.scan(FilterExpression=filter_expression)
           obj = response['Items'][0]
           eph_password = obj['password']
           if password == eph_password:
                pic_instance = DisplayPic()
                pic_request = pic_instance.get_presigned_url(obj['eph_id'][1:])
                if pic_request['successful']:
                    response = { 'successful': True, 'message': {'access_token': obj['access_token'], 'id': obj['id'], 'eph_id': obj['eph_id'], 'first_name': obj['first_name'], 'last_name': obj['last_name'], 'email': obj['email'], 'display_pic': pic_request["message"]}}
           else:
                response = { 'successful': False, 'message': 'Authentication Failed' }
            
        except Exception as e:
            response = { 'successful': False, 'message': str(e)}
        
        return response
    
    def create_user(self, first_name, last_name, email, password):
        table_name = 'x23211946_EphUsers'
        table = self.dyn_resource.Table(table_name)
        id_value = str(uuid.uuid4())
        
        scan = table.scan(Select='COUNT')
        item_count = scan['Count'] + 1
        hex_value = hex(item_count)[2:]
        eph_id = '#EP'+hex_value.zfill(3)
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
        
        filter_expression = Attr('eph_id').eq('#' + eph_id)
        
        try:
            response = table.scan(FilterExpression=filter_expression)
            item = response['Items'][0]
            if item:
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



    
        
