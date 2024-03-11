from django.http import JsonResponse

users = [
    {
        "id": "4b5c1c0e-041a-4e2c-bba3-0471200f1a5d",
        "ephemeral_Id": "X87654321",
        "password": "abc",
        "ephemeral_Name": "User_42"
    },
    {
        "id": "3a2d5f7a-81e9-4d76-8f48-82e89e2c4ae9",
        "ephemeral_Id": "X12345678",
        "password": "abc",
        "ephemeral_Name": "User_17"
    },
    {
        "id": "9c8b7a6d-2f1e-4c3d-96a5-9e8f7d6c5b4a",
        "ephemeral_Id": "X55555555",
        "password": "abc",
        "ephemeral_Name": "User_89"
    },
    {
        "id": "1e2a3a4c-d6f5-48e9-b1c0-efe1833bba99",
        "ephemeral_Id": "X98765432",
        "password": "abc",
        "ephemeral_Name": "User_73"
    }
]

def login_view(request, ephemeral_id, password):
    for user in users:
        if user["ephemeral_Id"] == ephemeral_id and user["password"] == password:
            return JsonResponse({'message': 'Login successful', 'user': user})

    return JsonResponse({'message': 'Login failed. Invalid credentials'})

def data_view(request):
    return JsonResponse(users, safe=False)
