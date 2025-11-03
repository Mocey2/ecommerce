# base/context_processors.py

from .models import InformationsSite

def informations_site(request):
    info = InformationsSite.objects.first()
    return {'infos_site': info}
