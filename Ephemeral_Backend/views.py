from django.http import JsonResponse

def data_view(request):
    return JsonResponse({ 'name': 'raghav'})
