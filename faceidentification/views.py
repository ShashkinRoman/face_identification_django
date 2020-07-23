from django.forms import modelformset_factory
from django.shortcuts import render, HttpResponse
# from faceidentification.models import Image_model
# Create your views here.
from django.views.decorators.http import require_http_methods
# from faceidentification.models import Addon
# from faceidentification.forms import AddonForm

def test_home_page(request):
    return render(request, template_name='test_home.html')

# @require_http_methods(['GET'])
# def addons(request, ):
#     addon_form_set = modelformset_factory(Addon, form=AddonForm, extra=1)
#     addon_forms = addon_form_set(queryset=Addon.objects.all())
#     return render(request, 'addons/addons.html', {'form': addon_forms})

