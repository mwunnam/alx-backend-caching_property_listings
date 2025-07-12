from django.core.cache import cache
from .models import Property

def getallproperties():
    properties = cache.get('all_properties')

    if not properties:
        properties = list(Property.objects.values())
        cache.set('all_property', properties, timeout=3600)

    return properties
