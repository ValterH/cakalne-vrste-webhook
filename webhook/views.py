from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = data['result']
        parameters = result['parameters']
        regionId = parameters['region']
        procedureId = parameters['procedure']
        urgencyId = parameters['urgency']

        speech = "ProcedureId: " + procedureId + " regionId: " + regionId + " urgencyId: " + urgencyId
        response = '{"speech": ' + speech + ',"displayText": '+ speech +',"source": "webhook"}'
        return HttpResponse(response)
    else:
        return HttpResponse("Method not allowed")
# Create your views here.
