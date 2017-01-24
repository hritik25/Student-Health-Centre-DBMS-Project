from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$' , views.index , name = 'index'),
	url(r'^addstudent/$',views.addStudent , name= 'addstudent'),
	url(r'^signin=(?P<q>\w+)/$', views.signin, name = 'signin'),
	url(r'^newentry/$', views.newentry, name = 'newentry'),
	url(r'^entries/$', views.entries , name = 'entries'),
	url(r'^studentdb/$', views.studentdb, name = 'studentdb'),
	url(r'^addstay/$', views.addStay, name = 'addstay'),
	url(r'^pathology/$', views.pathology, name = 'pathology'),
	url(r'^addbloodreport/$', views.addBloodReport , name = 'addbloodreport'),
	url(r'^addxrayreport/$', views.addXrayReport , name = 'addxrayreport'),
	url(r'^xray/$', views.Xray, name = 'xray'),
	url(r'^studentadmission/$', views.studentAdmission, name = 'studentadmission'),
	url(r'^(?P<q>\w+)/$', views.index , name = 'index'),
]