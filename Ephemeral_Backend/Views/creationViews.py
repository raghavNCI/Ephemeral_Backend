from django.http import JsonResponse
from Ephemeral_Backend.Dyno.users import Users
from Ephemeral_Backend.Dyno.peers import Peers
from Ephemeral_Backend.S3.displayPic import DisplayPic
from Ephemeral_Backend.Security.Client import client_token_required
from Ephemeral_Backend.Security.Access import access_token_required
import traceback
import json

@client_token_required
def create_user(request):
    try:
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
            
            if response['response']['ResponseMetadata']['HTTPStatusCode'] == 200:
                return JsonResponse({'successful': True, 'response': response})
            else:
                return JsonResponse({'successful': False, 'response': response})

        else:
            return JsonResponse({'successful': False, 'response': {'error': 'Unsupported HTTP method', 'status': 405}})
    except Exception as e:
        return JsonResponse({'successful': False, 'response': str(e)})

@access_token_required
def add_peer(request, addTo, addId):
    peer_instance = Peers()
    try:
        response = peer_instance.add_peer(addTo, addId)
        if response['successful']:
            temp = addTo
            addTo = addId
            addId = temp
            response = peer_instance.add_peer(addTo, addId)
    except Exception as e:
        response = {'successful': False, 'message': str(e)}
    
    return JsonResponse(response)

# @access_token_required    
def add_dp(request):
    try:
        if request.method == 'POST' and request.FILES.get('image'):
            image_file = request.FILES['image']
            image_data = image_file.read() 
            
            eph_id = request.POST.get('eph_id')[1:]
            if not eph_id:
                return JsonResponse({'successful': False, 'message': 'eph_id is required'}, status=400)

            display_pic = DisplayPic()
            response = display_pic.upload_dp_to_s3(image_data, eph_id)
            return JsonResponse(response)
        else:
            return JsonResponse({'successful': False, 'message': 'No image found'}, status=400)
    except Exception as e:
        traceback.print_exc()
        print(f'Error in add_dp: {e}')
        return JsonResponse({'successful': False, 'message': str(e)}, status=500)
    
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
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)