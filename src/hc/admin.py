from django.contrib import admin

# Register your models here.

from .models import Student , newEntry# , Doctor , SpecificDiagnosis , Medicine , Prescription , SupportStaff , Room , Bed

class StudentAdmin(admin.ModelAdmin):
	list_filter = ['faculty']
	class Meta:
		model = Student

# class BedAdmin(admin.ModelAdmin):
# 	list_filter = ['bed_type']
# 	class Meta:
# 		model = Bed

# class newEntryAdmin(admin.ModelAdmin):
# 	list_display = ['__unicode__' , 'admission_time' , 'updated']
# 	class Meta:
# 		model = newEntry

admin.site.register(Student , StudentAdmin)
admin.site.register(newEntry)
# admin.site.register(Bed , BedAdmin)
# admin.site.register(newEntry ,newEntryAdmin)
