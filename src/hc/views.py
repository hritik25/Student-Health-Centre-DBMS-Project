import datetime
from django.shortcuts import render,redirect , render_to_response
from django.http import HttpResponse
from .models import Student ,newEntry#, Doctor , SpecificDiagnosis , Bed
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


#this is for the admin-type widget
# from django.contrib import admin
# admin.autodiscover()
# from django.contrib.admin.widgets import ForeignKeyRawIdWidget

class addStudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'

class addStayForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
            super(addStayForm, self).__init__(*args, **kwargs)
            # Making fields required
            self.fields['stay_day'].required = True
            self.fields['stay_cause'].required = True
            self.fields['stay_bed'].required = True

    class Meta:
        model = newEntry
        fields = ['stay_day','stay_cause','stay_bed']


class addBloodReportForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
            super(addBloodReportForm, self).__init__(*args, **kwargs)
            # Making fields required
            self.fields['blood_test_report'].required = False
    
    class Meta:
        model = newEntry
        fields = ['blood_test_report']

class addXrayReportForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
            super(addXrayReportForm, self).__init__(*args, **kwargs)
            # Making fields required
            self.fields['xray_report'].required = False

    class Meta:
        model = newEntry
        fields = ['xray_report']

# class newEntryForm(forms.ModelForm):
#    	studentID = forms.ModelChoiceField(Student.objects.all(), widget=ForeignKeyRawIdWidget(newEntry._meta.get_field("student_id").rel,admin.site))
#    	doctor = forms.ModelChoiceField(Doctor.objects.all(), widget=ForeignKeyRawIdWidget(newEntry._meta.get_field("doctor").rel,admin.site))
#    	specificDiagnosis = forms.ModelChoiceField(SpecificDiagnosis.objects.all(), widget=ForeignKeyRawIdWidget(newEntry._meta.get_field("specificDiagnosis").rel,admin.site))
#    	bed = forms.ModelChoiceField(Bed.objects.all(), widget=ForeignKeyRawIdWidget(newEntry._meta.get_field("bed").rel,admin.site))
#    	class Meta:
#    		model = newEntry
#    		fields = ['studentID','doctor','specificDiagnosis','bed']

def index(request):
    #print '1'
    # if request.user.is_authenticated():
    #     return HttpResponse('Please log out first !')
    return render(request,'hc/index.html',{})

# def newentry(request):

# 	form = newEntryForm(request.POST or None) # "or none" for not running the validators
# 	context={
# 		"form":form,
# 	}
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.save()
		

# 		return	redirect('prescription')
# 	return	render(request,'hc/newentry.html',context)
# # Create your views here.
'''
def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('auth.html',{'state':state, 'username': username})
    '''
def signin(request, q):
  if request.method == 'POST':
    post = request.POST
    username = post['username']
    password = post['password']
    user = authenticate(username = username, password = password)
    if user is not None :
      login(request, user)
      if q == 'reception':
        return redirect('newentry')
      elif q == 'studentdb':
        print q
        return redirect('studentdb')
      elif q == 'stay':
        return redirect('studentadmission')
      elif q=='pathology':
        return redirect('pathology')
      elif q=='xray':
        return redirect('xray')

    else:
        return HttpResponse('Invalid Login')

  else:
    if request.user.is_authenticated():
        if request.user.username == 'reception':
            return redirect('newentry')
        elif request.user.username == 'studentdb':
            return redirect('studentdb')
        elif request.user.username == 'stay':
            return redirect('studentadmission')
        elif request.user.username=='pathology':
            return redirect('pathology')
        elif request.user.username=='xray':
            return redirect('xray')
    
    if q=='reception' or q == 'pathology' or q=='studentdb' or q=='stay' or q=='xray' :
        username = q
    
    return render(request, 'hc/signin.html', {'username': username})

@login_required(redirect_field_name = 'index')
def newentry(request):
    if request.method == 'POST':
        post = request.POST
        if 'new_entry' in post:
            try:
                student = Student.objects.get(roll_no = post['roll_no'])
                if student.diary_valid_through < datetime.date.today() :
                    return HttpResponse('The health diary of the student has expired , please ask the student to get his/her health diary renewed.')
                new_entry = newEntry(student_id = student , last_updated_by = request.user.username)
                new_entry.save()
                return render(request, 'hc/new.html', {'entry': new_entry})
            except ObjectDoesNotExist:
                return HttpResponse('Roll No. Invalid or Student is not registered with the Health Centre')
        elif 'logout' in post:
            logout(request)
            return redirect('index')
    else:
        if request.user.username == 'reception':
            return render(request, 'hc/newentry.html')

@login_required(redirect_field_name = 'index')
def studentdb(request):
    if request.method == 'POST' :
        post = request.POST
        if 'logout' in post:
            logout(request)
            return redirect('index')

        elif 'show' in post:
            try:
                student = Student.objects.get(roll_no = post['roll_no'])
                if student.diary_valid_through < datetime.date.today() :
                    validity_issue = "The validity of the student's health diary has expired , please get it renewed !"
                else:
                    validity_issue = ""

                return render(request, 'hc/studentinfo.html', {'student': student , 'validity_issue' : validity_issue})

            except ObjectDoesNotExist:
                return HttpResponse('Roll No. Invalid or Student is not registered with the Health Centre')

        elif 'renew' in  post:
            student = Student.objects.get(roll_no = post['renew']) 
            current_month = datetime.date.today().month
            current_year = datetime.date.today().year

            if current_month >= 1 and current_month <=6:
                valid_through_year = current_year
            else :
                valid_through_year = current_year + 1

            defaul_validity = str(valid_through_year) + '0630'
            student.diary_valid_through = datetime.datetime.strptime(defaul_validity , "%Y%m%d")
            student.save()
            return render(request , 'hc/renewed.html')

    elif request.user.username != 'studentdb':
        return HttpResponse('Please log out from %s first !' %(request.user.username))
    elif request.user.username == 'studentdb':
        return render(request, 'hc/studentdb.html')

@login_required(redirect_field_name = 'index')
def entries(request):
    if request.method == 'POST':
        post = request.POST
        if 'search-by-roll' in post:
            entries = newEntry.objects.filter(student_id__roll_no = post['roll_no'])
            if entries.count()>0:
                reference = 'Entries for Roll No. %s' %(post['roll_no'])
            else:
                try:
                    Student.objects.get(roll_no = post['roll_no'])
                    reference = 'No entries for Roll No. %s' %(post['roll_no'])
                except ObjectDoesNotExist:
                    return HttpResponse('Roll No. Invallid or Student is not registered with the Health Centre')


        elif 'search-by-date' in post:
            reference = post['date']
            x = datetime.datetime.strptime(post['date'] , '%Y-%m-%d')
            entries = newEntry.objects.filter(Q(entry_time__year = x.year) & Q(entry_time__month = x.month) & Q(entry_time__day = x.day))
            if entries.count()>0:
                reference = 'Entries for Date: %s' %(post['date'])
            else:
                reference = '%s : No entries were created' %(post['date'])

        elif 'back' in post:
            return redirect('newentry')
    else:
        if request.user.username != 'reception':
            return HttpResponse('Please log out from' '"%s"' 'first !' %(request.user.username))
        if request.user.username == 'reception':
            entries = newEntry.objects.filter(entry_time__day = datetime.date.today().day)
            print entries.count()
            if entries.count()>0:
                reference = 'Entries for Today: '
            else:
                reference = 'No entries have been created Today '

    return render(request, 'hc/entries.html', {'entries': reversed(entries) ,'reference' : reference})

@login_required(redirect_field_name = 'index')
def addStudent(request):
    form = addStudentForm(request.POST or None) # "or none" for not running the validators
    context={
        "form":form,
    }

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        

        return  render(request , 'hc/studentadded.html')
    return  render(request,'hc/addstudent.html',context)

@login_required(redirect_field_name = 'index')
def studentAdmission(request):
    if request.method == 'POST':
        post = request.POST
        if 'search' in post:
            entries = newEntry.objects.filter(student_id__roll_no = post['roll_no'])
            if entries.count()>0:
                reference = 'Entries for Roll No. %s . Select the entry to add stay to :' %(post['roll_no'])
            else:
                try:
                    Student.objects.get(roll_no = post['roll_no'])
                    reference = 'No entries for Roll No. %s' %(post['roll_no'])
                except ObjectDoesNotExist:
                    return HttpResponse('Roll No. Invallid or Student is not registered with the Health Centre')
        
        elif 'select_entry' in post:
            request.session['entry_id'] = post['select_entry']
            return redirect('addstay')

        elif 'logout' in post:
            logout(request)
            return redirect('index')


    else:
        if request.user.username != 'stay':
            return HttpResponse('Please log out from' '"%s"' 'first !' %(request.user.username))
        if request.user.username == 'stay':
            entries = []
            return render(request , 'hc/studentadmission.html')

    return render(request, 'hc/studentadmission.html', {'entries': reversed(entries) ,'reference' : reference})


@login_required(redirect_field_name = 'index')
def addStay(request):

    form = addStayForm(request.POST or None)
    context = {
        "form":form,
    }

    if form.is_valid():
        instance = form.save(commit = False)
        entry = newEntry.objects.get(id = request.session["entry_id"])
        entry.last_updated_by = request.user.username
        entry.stay_day = instance.stay_day
        entry.stay_cause = instance.stay_cause
        entry.stay_bed = instance.stay_bed
        entry.save()
        del request.session['entry_id']

        return render(request , 'hc/discharged.html' , {'roll_no' : entry.student_id})

    if 'entry_id' in request.session:
        return render(request , 'hc/stay.html' , context)
    else :
        return HttpResponse('Please select entry to be updated first! ')


@login_required(redirect_field_name = 'index')
def pathology(request):
    if request.method == 'POST':
        post = request.POST

        if 'logout' in post:
            print "logout"
            logout(request)
            return redirect('index')

        if 'search-by-roll' in post:
            entries = newEntry.objects.filter(Q(student_id__roll_no = post['roll_no']) & Q(entry_time__day = datetime.date.today().day))
            if entries.count()>0:
                reference = 'Entries for Roll No. %s created today' %(post['roll_no'])
            else:
                try:
                    Student.objects.get(roll_no = post['roll_no'])
                    reference = 'No entries for Roll No. %s Today' %(post['roll_no'])
                except ObjectDoesNotExist:
                    return HttpResponse('Roll No. Invallid or Student is not registered with the Health Centre')

        elif 'select_entry' in post:
            request.session['entry_id'] = post['select_entry']
            return redirect('addbloodreport')

    else:

        if request.user.username != 'pathology':
            return HttpResponse('Please log out from' '"%s"' 'first !' %(request.user.username))
        if request.user.username == 'pathology':
            entries = newEntry.objects.filter(entry_time__day = datetime.date.today().day)
            if entries.count()>0:
                reference = "Today's entries: "
            else:
                reference = 'No entries have been created Today'

    return render(request, 'hc/pathology.html', {'entries': reversed(entries) ,'reference' : reference})


@login_required(redirect_field_name = 'index')
def addBloodReport(request):
    form = addBloodReportForm(request.POST or None)
    
    if request.method == 'POST':
        post = request.POST
        file1 = request.FILES
        print post
        print file1['blood_report']
        entry = newEntry.objects.get(id = request.session["entry_id"])
        entry.last_updated_by = request.user.username
        entry.blood_test_report = file1['blood_report']
        entry.save()
        del request.session['entry_id']
        return render(request , 'hc/badded.html')


    if 'entry_id' in request.session:
        return render(request , 'hc/bloodreport.html' , {'form' : form})
    else :
        return HttpResponse('Please select entry to be updated first! ')


@login_required(redirect_field_name = 'index')
def Xray(request):
    if request.method == 'POST':
        post = request.POST

        if 'select_entry' in post:
            request.session['entry_id'] = post['select_entry']
            return redirect('addxrayreport')

        if 'search-by-roll' in post:
            entries = newEntry.objects.filter(Q(student_id__roll_no = post['roll_no']) & Q(entry_time__day = datetime.date.today().day))
            if entries.count()>0:
                reference = 'Entries for Roll No. %s created today' %(post['roll_no'])
            else:
                try:
                    Student.objects.get(roll_no = post['roll_no'])
                    reference = 'No entries for Roll No. %s Today' %(post['roll_no'])
                except ObjectDoesNotExist:
                    return HttpResponse('Roll No. Invallid or Student is not registered with the Health Centre')

        elif 'logout' in post:
            logout(request)
            return redirect('index')

    else:

        if request.user.username != 'xray':
            return HttpResponse('Please log out from' '"%s"' 'first !' %(request.user.username))
        if request.user.username == 'xray':
            entries = newEntry.objects.filter(entry_time__day = datetime.date.today().day)
            if entries.count()>0:
                reference = "Today's entries:"
            else:
                reference = 'No entries have been created Today '

    return render(request, 'hc/xray.html', {'entries': reversed(entries) ,'reference' : reference})

@login_required(redirect_field_name = 'index')
def addXrayReport(request):
    form = addXrayReportForm(request.POST or None)
    
    if request.method == 'POST':
        post = request.POST
        file1 = request.FILES
        print post
        print file1['xray_report']
        entry = newEntry.objects.get(id = request.session["entry_id"])
        entry.last_updated_by = request.user.username
        entry.xray_report = file1['xray_report']
        entry.save()
        del request.session['entry_id']
        return render(request , 'hc/xadded.html')

    if 'entry_id' in request.session:
        return render(request , 'hc/xrayreport.html' , {'form':form})
    else :
        return HttpResponse('Please select entry to be updated first! ')