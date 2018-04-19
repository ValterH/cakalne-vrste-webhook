from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from webhook.models import Procedure, Urgency, Region, Group
import requests
import json
import re

@csrf_exempt
<<<<<<< HEAD
def webhook(request):
=======
def index(request):
>>>>>>> 4889137c9afbc77ec3b998fb8facffca04a44ac4
    if request.method == 'POST':
        data = get_data(request)
        if(data[3] != "" and data[0] == ""): 
            data_field = choose_procedure(data[3])
            return JsonResponse({"fulfillmentText": "Izberi poseg",
                                 "source": "https://glacial-journey-77420.herokuapp.com/webhook/",
                                 "payload":{"responseType":"waitingTimes",
                                           "data":data_field,
                                           "url":""
                                          }
                               })
        if(data[0] == ""): return JsonResponse({"fulfillmentText": "Kateri poseg iščete?",
                                                "source": "https://glacial-journey-77420.herokuapp.com/webhook/",
                                              })
        if(data[2] == "A"): data[2] = ""
        query = firstfive(scrape(data[0],data[1],data[2]))
        speech = "Storitev ni na voljo."
        if(len(query)>1): speech = "Našel sem naslednje posege..."
        data_field = to_data(query)

        return JsonResponse({"fulfillmentText": speech,
                             "source": "https://glacial-journey-77420.herokuapp.com/webhook/",
                             "payload":{"responseType":"waitingTimes",
                                        "data":data_field,
                                        "url":""
                                    }
                             })
    else:
        return HttpResponse("Method not allowed")

def choose_procedure(group_name):
  array=[]
  group=Group.objects.filter(name__icontains=group_name).get()
  procedures = Procedure.objects.filter(group = group.id)
  for procedure in procedures:
    dict={}
    dict['name']=procedure.name
    dict['value']=procedure.procedure_id
    array.append(dict)
  return array

def get_data(request):
    data = json.loads(request.body)
    result = data['queryResult']
    parameters = result['parameters']
    return [parameters['procedure'],parameters['urgency'],parameters['region'],parameters['group']]

def scrape(pro, urg, reg):
        d = {'procedureId': pro, 'urgencyTypeIdp': urg, 'regionId': reg, 'btnProcedureSubmit': ''}
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
            
        error = ""
        if ime == []:
            err = soup.find('div',{"class":"col-md-12 error message-error"})
            if(err!=None): error = err.text.strip()
        
        return [postopek, ime,okvirni_termin,cakalna_doba,telefon,email,error]

def firstfive(data):
        if(data[6] != ""):
            return [data[6]]
        else:
            return [data[0],data[1][:6],data[2][:6],data[3][:6],data[4][:6],data[5][:6]]

def to_speech(data): # Samo za testiranje
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
    return r

def to_data(data):
  if(len(data)==1): return {'message':data[0]}
  return add_procedures(data[1:])

def get_procedures(request):
    procedures=Procedure.objects.all()
    array=[]
    for procedure in procedures:
        json_obj={}
        json_obj['name']=procedure.name
        json_obj['id']=procedure.procedure_id
        array.append(json_obj)
    return JsonResponse({'procedures':array})

def get_regions(request):
    regions=Region.objects.all()
    array=[]
    for region in regions:
        json_obj={}
        json_obj['name']=region.name
        json_obj['id']=region.region_id
        array.append(json_obj)
    return JsonResponse({'regions':array})

def get_urgency(request):
    urgencies=Urgency.objects.all()
    array=[]
    for urgency in urgencies:
        json_obj={}
        json_obj['name']=urgency.name
        json_obj['id']=urgency.urgency_id
        array.append(json_obj)
    return JsonResponse({"urgencies":array})

def get_waiting_times(request,pro,urg,reg):
    data = firstfive(scrape(pro,urg,reg))
    if(len(data)==1): return JsonResponse({'message':data[0]})
    info = data[0].splitlines()
    response=add_info(info)
    response['services']=add_procedures(data[1:])
    return JsonResponse(response)

def waiting_times_no_region(request, pro, urg):
    return get_waiting_times(request,pro,urg,"")

def add_info(i):
    dict={}
    procedure=i[1].split(":")
    urgency=i[3].split(":")
    region=i[5].split(":")
    dict['procedure']=procedure[1].strip()
    dict['urgency']=urgency[1].strip()
    dict['region']=region[1].strip()
    return dict

def add_procedures(data):
    array=[]
    for i in range(0,len(data[0])):
        array.append(tojson([data[0][i],data[1][i],data[2][i],data[3][i],data[4][i]]))
    return array

def tojson(d):
    dict={}
    dict['hospital']=d[0]
    dict['phone']=d[3]
    dict['email']=d[4]
    dict['reception']=reception([d[1],d[2]])
    return dict

def reception(d):
    dict={}
    if(d[0]=="Prvi razpoložljivi termin"): 
      dict['avilability']="Prost Sprejem"
      dict['days_to']="0"
      return dict
    if(d[0]=="Okvirni termin"):
      dict['avilability']=d[1]
      dict['days_to']= d[1]     #Izračunaj dneve do (npr. prva polovica maja)
      return dict
    termin = d[0].split(": ")
    dnevi = d[1].split(": ")
    dict['availability']=termin[1]
    dict['daysTo']=dnevi[1]
    return dict

# DATABASE
def update_db(request):
    db_update_procedures()
    db_update_urgencies()
    db_update_regions()
    db_update_groups()
    #proceduresJson()
    #groupsJson()
    return HttpResponse("Database Updated")

def db_update_procedures():
    url = "https://cakalnedobe.ezdrav.si/Home/GetProcedures"
    procedures = json.loads(requests.get(url).text)
    Procedure.objects.all().delete()
    for procedure in procedures:
        new_procedure=Procedure(name=procedure['Name'], procedure_id=procedure['Id'])
        new_procedure.save()
    print("--Procedures updated")
    return

def db_update_urgencies():
    url = "https://cakalnedobe.ezdrav.si/"
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    urgencies = soup.find_all('option')[0:3]
    Urgency.objects.all().delete() 
    for urgency in urgencies:
        new_urgency=Urgency(name=urgency.text, urgency_id=urgency['value'])
        new_urgency.save()
    print("--Urgencies updated")
    return

def db_update_regions():
    url = "https://cakalnedobe.ezdrav.si/"
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    options = soup.find_all('option')
    regions = options[3:len(options)-3]
    Region.objects.all().delete()
    for region in regions:
        new_region=Region(name=region.text, region_id=region['value'])
        new_region.save()
    print("--Regions updated")
    return

def db_update_groups():
  Group.objects.all().delete()

  #head scan
  procedures=Procedure.objects.filter(name__icontains="glave").exclude(name__icontains="operacije")
  add_group("head scan",procedures)
  #operation
  procedures=Procedure.objects.filter(name__icontains="operacija ")|Procedure.objects.filter(name__icontains="operacije")
  procedures=procedures.exclude(name__icontains="razen operacije")
  add_group("operation",procedures)
  #biopsy
  procedures=Procedure.objects.filter(name__icontains="biopsij").exclude(name__icontains="porodništvu")
  add_group("biopsy",procedures)
  #MR and MRA
  procedures=Procedure.objects.filter(name__icontains="MR").exclude(name__icontains="mre")
  add_group("MR and MRA",procedures)
  #surgical examination
  procedures=Procedure.objects.filter(name__icontains="kirurški pregled")
  add_group("surgical examination",procedures)
  #CT and CTA
  procedures=Procedure.objects.filter(name__icontains="CT").exclude(name__icontains="OCT")
  add_group("CT and CTA",procedures)
  #arthrodesis
  procedures=Procedure.objects.filter(name__icontains="artrodeza")
  add_group("arthrodesis",procedures)
  #removal
  procedures=Procedure.objects.filter(name__icontains="odstran")
  add_group("removal",procedures)
  #rentgen
  procedures=Procedure.objects.filter(name__icontains="RTG")
  add_group("rentgen",procedures)
  #review
  procedures=Procedure.objects.filter(name__icontains="Pregled")
  add_group("review",procedures)
  #other procedures
  procedures=Procedure.objects.filter(name__icontains="Drugi posegi")|Procedure.objects.filter(name__icontains="Druge")
  add_group("other procedures",procedures)
  #ostheosynthesis
  procedures=Procedure.objects.filter(name__icontains="Osteosinteza")
  add_group("ostheosynthesis",procedures)
  #scintigraphy
  procedures=Procedure.objects.filter(name__icontains="Scintigrafija")
  add_group("scintigraphy",procedures)
  #ultrasound
  procedures=Procedure.objects.filter(name__icontains="UZ")|Procedure.objects.filter(name__icontains="ultrazvo")
  procedures=procedures.exclude(name__icontains="uzi")
  add_group("ultrasound",procedures)
  #transplant
  procedures=Procedure.objects.filter(name__icontains="transplantacija")|Procedure.objects.filter(name__icontains="presejanje")
  add_group("transplant",procedures)
  #revision
  procedures=Procedure.objects.filter(name__icontains="revizij")
  add_group("revision",procedures)
  #intervention
  procedures=Procedure.objects.filter(name__icontains="poseg")
  add_group("intervention",procedures)
  #insertion
  procedures=Procedure.objects.filter(name__icontains="vstavitev")
  add_group("insertion",procedures)
  #treatement
  procedures=Procedure.objects.filter(name__icontains="zdravljenje")|Procedure.objects.filter(name__icontains="obravnava")
  add_group("treatement",procedures)
  #reconstruction
  procedures=Procedure.objects.filter(name__icontains="rekonstrukcij")
  add_group("reconstruction",procedures)
  #arthroscopy
  procedures=Procedure.objects.filter(name__icontains="artroskopija")
  add_group("arthroscopy",procedures)
  #manometry
  procedures=Procedure.objects.filter(name__icontains="manometrija")
  add_group("manometry",procedures)
  #test
  procedures=Procedure.objects.filter(name__icontains="test")|Procedure.objects.filter(name__icontains="preiskav")|Procedure.objects.filter(name__icontains="ocena")|Procedure.objects.filter(name__icontains="monitor")
  add_group("test",procedures)
  #excision
  procedures=Procedure.objects.filter(name__icontains="ekscizija")
  add_group("excision",procedures)
  #echocardiography
  procedures=Procedure.objects.filter(name__icontains="ehokardiografija")
  add_group("echocardiography",procedures)
  #outside
  procedures=Procedure.objects.filter(name__icontains="zuna")
  add_group("outside",procedures)
  #rehabilitation
  procedures=Procedure.objects.filter(name__icontains="rehabilitacija")
  add_group("rehabilitation",procedures)
  #measuring
  procedures=Procedure.objects.filter(name__icontains="merit")|Procedure.objects.filter(name__icontains="merje")
  procedures=procedures.exclude(name__icontains="usmerjen")
  add_group("measuring",procedures)
  #endoprothesis
  procedures=Procedure.objects.filter(name__icontains="endoproteza")
  add_group("endoprothesis",procedures)
  #percutaneous
  procedures=Procedure.objects.filter(name__icontains="perkutana")
  add_group("percutaneous",procedures)
  #teeth
  procedures=Procedure.objects.filter(name__icontains="zob")
  add_group("teeth",procedures)
  #head
  procedures=Procedure.objects.filter(name__icontains="glave")|Procedure.objects.filter(name__icontains="lobanje")
  add_group("head",procedures)
  #amputation
  procedures=Procedure.objects.filter(name__icontains="amputacija")
  add_group("amputation",procedures)
  #cathether
  procedures=Procedure.objects.filter(name__icontains="kateter")
  add_group("cathether",procedures)
  #adjustment
  procedures=Procedure.objects.filter(name__icontains="naravnava")
  add_group("adjustment",procedures)
  #heart
  procedures=Procedure.objects.filter(name__icontains="src")|Procedure.objects.filter(name__icontains="srč")
  add_group("heart",procedures)
  #skin
  procedures=Procedure.objects.filter(name__icontains="kož")
  add_group("skin",procedures)
  #lungs
  procedures=Procedure.objects.filter(name__icontains="pljuč")
  add_group("lungs",procedures)
  #ph meter
  procedures=Procedure.objects.filter(name__icontains="ph met")|Procedure.objects.filter(name__icontains="ph-met")
  add_group("ph meter",procedures)
  #Doppler
  procedures=Procedure.objects.filter(name__icontains="Doppler")
  add_group("Doppler",procedures)
  #implantation
  procedures=Procedure.objects.filter(name__icontains="implantacija")
  add_group("implantation",procedures)
  #correction
  procedures=Procedure.objects.filter(name__icontains="korekci")
  add_group("correction",procedures)

  print("--Groups updated")
  #test
  #pro=Procedure.objects.filter(group=None)
  #f = open('proceduresNoGroup.txt','w')
  #i = 0
  #for p in pro: 
  #      f.write(str(p.name) + " : " + str(p.procedure_id) + '\n')
  #      i+=1
  #f.close()
  #print(str(i) + " posegov brez kategorij")
  return

def add_group(group_name, queryset):
    new_group=Group(name=group_name)
    new_group.save()
    for procedure in queryset:
        procedure.group_set.add(new_group)
    return

def add_group_test(group_name, queryset):
    new_group=Group(name=group_name)
    new_group.save()
    for procedure in queryset:
        print(procedure.name)
        procedure.group_set.add(new_group)
    return

# entities json
def translate(input):
    url = "http://translate.dis-apps.ijs.si/translate?sentence="+input
    req = requests.get(url)
    return req.text[1:-3]

def proceduresJson():
    entries = []
    procedures=Procedure.objects.all()
    for procedure in procedures:
        entries.append({'value':procedure.procedure_id,'synonyms':[translate(procedure.name)]})
    data = {'automatedExpansion': False,
            'entries': entries,
            'isEnum':False,
            'isOverridable':True,
            'name':'procedure_test'
            }
    with open('procedures.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    f.close()
    # na dialogflow so appendani \n ???
    return

def groupsJson():
    entries = []
    groups=Group.objects.all()
    for group in groups:
        entries.append({'value':group.name,'synonyms':[group.name]})
    data = {'name':'group_test',
            'automatedExpansion': False,
            'entries': entries,
            'isEnum':False,
            'isOverridable':True
            }
    with open('groups.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    f.close()
    return

  