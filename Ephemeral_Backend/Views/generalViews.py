from django.http import JsonResponse
from Ephemeral_Backend.Dyno.users import Users
from Ephemeral_Backend.Dyno.peers import Peers
from Ephemeral_Backend.S3.displayPic import DisplayPic

def test_view(request):
    return JsonResponse({'message': 'App working successfully'})

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

def get_user(request, eph_id):
    inst = Users()
    response = inst.get_user(eph_id)
    return JsonResponse(response)

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
        
