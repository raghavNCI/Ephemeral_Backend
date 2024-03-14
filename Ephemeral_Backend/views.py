from django.http import JsonResponse
from .dynoDb import Users

def test_view(request):
    return JsonResponse({'message': 'App working successfully'})

def login_view(request, ephemeral_id, password):
    for user in users:
        if user["ephemeral_Id"] == ephemeral_id and user["password"] == password:
            return JsonResponse({'message': 'Login successful', 'user': user})

    return JsonResponse({'message': 'Login failed. Invalid credentials'})

def create_user_table(request):
    user_instance = Users()
    user_instance.create_table()

    return JsonResponse({'message': f'Table created successfully!'})
