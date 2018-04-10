from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import requests
import json
import re

@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = get_data(request)
        if(data[3] != "" and data[0] == ""): 
            speech = izberi_poseg(data[3])
            return JsonResponse( {"speech": speech, "displayText": speech,})
        if(data[0] == ""): return JsonResponse( {"speech": "Kateri poseg iščete?", "displayText": "Kateri poseg iščete?"})
        if(data[2] == "A"): data[2] = ""
        query = firstfive(scrape(data[0],data[1],data[2]))
        speech = dataToStr(query)

        return JsonResponse( {"speech": speech, "displayText": speech})
    else:
        return HttpResponse("Method not allowed")

def izberi_poseg(group):
    groups = {'head scan':["rentgen glave",
                           "MR glave(kontrast)",
                           "MR glave (brez kontrasta)",
                           "spektroskopija glave",
                           "ultrazvok glave",
                           "ultrazvok otroške glave"]
              }
    res = "izberi:\n"
    for procedure in groups[group]:
        res += procedure + "\n"
    return res

def get_data(request):
    data = json.loads(request.body)
    result = data['result']
    parameters = result['parameters']
    return [parameters['procedure'],parameters['urgency'],parameters['region'],parameters['group']]

def scrape(pro, urg, reg):
        d = {'procedureId': pro, 'urgencyTypeIdp': urg, 'regionId': reg, 'btnProcedureSubmit': ''}
        # request traja dolgo
        req = requests.post("https://cakalnedobe.ezdrav.si/Home/ProcedureAppointmentSlots", data=d)
        html = req.text
        soup = BeautifulSoup(html,"html.parser")
        klinike = soup.find_all('div',{"class":"col-md-10 col-md-offset-1 well"})
        p = soup.find('h4')
        postopek = p.text
        c = 0
        ime = []
        cakalna_doba = []
        okvirni_termin = []
        email = []
        telefon = []
        for k in klinike:
            i = k.find('a').getText()
            ime.append(i)
    
            co1 = k.find_all('div',{"class":"row slotHeader"})
            co2 = k.find_all('div',{"class":"row slotData"})
            if (len(co1) > 1):
                ot = co1[0].text.strip() + ": " + co2[0].text.strip()
                cd = co1[1].text.strip() + ": " + co2[1].text.strip()
            else:
                ot = co1[0].text.strip()
                cd = co2[0].text.strip()
            okvirni_termin.append(ot.replace('\n',''))
            cakalna_doba.append(cd.replace('\n',''))

            teem = k.find_all('div',{"class":"col-md-6 propValue"})
            nt = True
            ne = True
            for te in teem:
                et = te.text.strip()
                if et.find("@") != -1:
                    ne = False
                    email.append(et)
                
                tel = re.findall(r'[\+\]?[1-9][0-9 \-\(\)]{8,}[0-9]', et)
                if(len(tel)>0):
                    telefon.append(et)
                    nt = False
                    break
            if(nt): telefon.append("telefon ni podan")
            if(ne): email.append("email ni podan")
            c+=1
            
        err = ""
        if ime == []:
            err = soup.find('div',{"class":"col-md-12 error message-error"}).text.strip()
        
        return [postopek, ime,okvirni_termin,cakalna_doba,telefon,email,err]

def firstfive(data):
        if(data[6] != ""):
            return [data[6]]
        else:
            return [data[0],data[1][:6],data[2][:6],data[3][:6],data[4][:6],data[5][:6]]

def dataToStr(data):
    r =r""
    r += str(data[0]) + '\n'
    r += '\n'
    if(len(data)>1):
            for i, n in enumerate(data[1]):
                r += str(data[1][i]) + '\n'
                r += str(data[2][i]) + '\n'
                r += str(data[3][i]) + '\n'
                r += str(data[4][i]) + '\n'
                r += str(data[5][i]) + '\n'
                r += '\n'
    print(r)
    return r
