from django.http import JsonResponse
from Dyno.users import Users
from Dyno.peers import Peers
from S3.displayPic import DisplayPic
from Security.Client import client_token_required
from Security.Access import access_token_required

def test_view(request):
    return JsonResponse({'message': 'App working successfully'})
    
@client_token_required
def login_view(request, ephemeral_id, password):
    inst = Users()
    eph_id = ephemeral_id
    response = inst.auth_user(eph_id, password)
    
    return JsonResponse(response)

def create_user_table(request):
    user_instance = Users()
    response = user_instance.create_table()

    return JsonResponse(response)
    
def create_peer_table(request):
    peer_instance = Peers()
    response = peer_instance.create_table()
    
    return JsonResponse(response)

# @access_token_required
def get_user(request, eph_id):
    try:
        inst = Users()
        print('Working here')
        response = inst.get_user(eph_id)
        return JsonResponse(response)
    except Exception as e:
        response = {'successful': False, 'message': str(e)}
        return JsonResponse(response)

# @access_token_required
def get_peers(request, eph_id):
    inst = Peers()
    response = inst.get_peers(eph_id)
    return JsonResponse(response)

def create_displayPic_Bucket(request):
    try:
        instance = DisplayPic()
        response = instance.createDPBucket()
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({'successful': False, 'message': str(e)})
        
