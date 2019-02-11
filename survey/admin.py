from django.contrib import admin
from .models import Organization, Questions_library, Survey, Survey_QuesMap, SurveyEmployeeMap

# Register your models here.
admin.site.register(Organization)
admin.site.register(Questions_library)
admin.site.register(Survey)
admin.site.register(Survey_QuesMap)
admin.site.register(SurveyEmployeeMap)
