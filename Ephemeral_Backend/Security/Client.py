from django.http import JsonResponse

def client_token_required(func):
    def wrapper(request, *args, **kwargs):
        client_token = request.headers.get('Client-Token')
        if client_token != 'A7b9Fg2HtR4jKl6Mn8Pq9Sv3Uw5Yz7X':
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        return func(request, *args, **kwargs)
    return wrapper