from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property
from .utils import getallproperties

@cache_page(60 * 15)
def property_list(request):
    properties = getallproperties()
    return JsonResponse({"data": properties})
