from django.conf import settings


def legal(request):
    return {
        'LEGAL_ENABLED': settings.LEGAL_ENABLED,
    }
