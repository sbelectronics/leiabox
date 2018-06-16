from django.shortcuts import render
from django.template import RequestContext, loader
import json

from leiabox_manager import glo_leiabox

# Create your views here.

from django.http import HttpResponse

def index(request):
    template = loader.get_template('leiabox_web_ui/index.html')
    context = RequestContext(request, {});
    return HttpResponse(template.render(context))

def setProgram(request):
    value = request.GET.get("value", 0)

    glo_leiabox.set_program(int(value))

    return HttpResponse("okey dokey")

def setVolume(request):
    value = request.GET.get("value", 0)

    glo_leiabox.set_volume(v=int(value))

    return HttpResponse("okey dokey")

def getStatus(request):
    result = {}

    result["program"] = glo_leiabox.get_program()
    result["volume"] = glo_leiabox.get_volume()

    return HttpResponse(json.dumps(result), content_type='application/javascript')
