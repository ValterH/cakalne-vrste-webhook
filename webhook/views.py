from django.shortcuts import render, HttpResponse
def index(request):
    if request.method == 'POST':
        result = request.POST.get('result')
        parameters = result.get('parameters')
        regionId = parameters.get('region')
        procedureId = parameters.get('procedure')
        urgencyId = parameters.get('urgency')

        return HttpResponse("{'speech':'', 'displayText':'', 'source':'webhook'}")
    else:
        return HttpResponse("Method not allowed")
# Create your views here.
