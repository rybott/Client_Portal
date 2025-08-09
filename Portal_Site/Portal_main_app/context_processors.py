from .models import Case

def open_cases(request):
    return {
        'open_cases': Case.objects.exclude(stage='closed')
    }