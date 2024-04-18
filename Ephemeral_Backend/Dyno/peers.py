import boto3
from boto3.dynamodb.conditions import Attr, Key
from Ephemeral_Backend.Dyno.users import Users

dyn_resource = boto3.resource('dynamodb', 'eu-west-1')

class Peers:
    
    def __init__(self):
        self.dyn_resource = dyn_resource
        self.table = None
        
    def create_table(self):
        self.table = self.dyn_resource.create_table(
            TableName='x23211946_EphPeers',
            KeySchema=[
                {'AttributeName': 'eph_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'eph_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        
    def get_peers(self, eph_id):
        table_name = 'x23211946_EphPeers'
        table = self.dyn_resource.Table(table_name)
        
        try:
            response = table.get_item(Key={'eph_id': eph_id})
            item = response.get('Item')
            
            if item:
                peers = item.get('peers', [])
                peerInfo = []
                
                for peer_eph_id in peers:
                    users = Users();
                    response = users.get_user(peer_eph_id)
                    if response['successful']:
                        peerInfo.append(response['item'])
                    else:
                        peerInfo.append({
                            'eph_id': peer_eph_id
                        }) 
                
                return {'successful': True, 'peerInfo': peerInfo}
            else:
                return {'successful': False, 'message': f"No item found for eph_id: {eph_id}"}
        except Exception as e:
            return {'successful': False, 'message': str(e)}


    
    def add_peer(self, addTo, addId):
        table_name = 'x23211946_EphPeers'
        table = self.dyn_resource.Table(table_name)
    
        try:
            response = table.get_item(Key={'eph_id': addTo})
            item = response.get('Item')
    
            if item is None:
                item_data = {'eph_id': addTo, 'peers': []}
                table.put_item(Item=item_data)
                item = item_data  # Update item with the newly created item
    
            peers = item.get('peers', [])
    
            addId_dynamodb = addId
            if addId_dynamodb not in peers:
                peers.append(addId_dynamodb)
                table.update_item(
                    Key={'eph_id': addTo},
                    UpdateExpression='SET peers = :val',
                    ExpressionAttributeValues={':val': peers}
                )
                return {'successful': True, 'message': 'Peer added successfully'}
            else:
                return {'successful': False, 'message': 'Peer already exists'}
    
        except Exception as e:
            return {'successful': False, 'message': str(e)}
        
    def delete_peer(self, removeFrom, removeId):
        table_name = 'x23211946_EphPeers'
        table = self.dyn_resource.Table(table_name)
    
        try:
            response = table.get_item(Key={'eph_id': removeFrom})
            item = response.get('Item')
    
            if item is None:
                return {'successful': False, 'message': 'No such peer found to remove'}
    
            peers = item.get('peers', [])
    
            if removeId in peers:
                peers.remove(removeId)
                
                table.update_item(
                    Key={'eph_id': removeFrom},
                    UpdateExpression='SET peers = :val',
                    ExpressionAttributeValues={':val': peers}
                )
                return {'successful': True, 'message': 'Peer removed successfully'}
            else:
                return {'successful': False, 'message': 'Peer not found in the list'}
    
        except Exception as e:
            return {'successful': False, 'message': str(e)}




        