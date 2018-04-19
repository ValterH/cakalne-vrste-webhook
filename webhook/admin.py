from django.contrib import admin
from webhook.models import *

admin.site.register([Procedure, Urgency, Region, Group])