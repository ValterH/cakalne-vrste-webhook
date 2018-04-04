from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def index(request):
    if request.method == 'POST':
        result = request.POST.get('result')
        parameters = result.get('parameters')
        regionId = parameters.get('region')
        procedureId = parameters.get('procedure')
        urgencyId = parameters.get('urgency')

        speech = "ProcedureId: " + procedureId + " regionId: " + regionId + " urgencyId: " + urgencyId
        return {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            #"contextOut": [],
            "source": "webhook"
    }
    else:
        return HttpResponse("Method not allowed")
# Create your views here.
