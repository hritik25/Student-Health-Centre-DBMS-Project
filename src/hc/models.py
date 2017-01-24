import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


phone_regex = RegexValidator ( 
		regex=r'^\+?1?\d{10,10}$',
		message="Phone number must be a valid 10 digit number."
	)

class Student(models.Model):
	roll_no = models.CharField('Student ID No.', max_length = 10 , primary_key = True)
	full_name = models.CharField(max_length = 30)
	GENDER = (('M' , 'Male'), 
		('F' , 'Female') ,
	)
	gender = models.CharField(max_length = 1 , choices = GENDER)
	FACULTY = (('CSE', 'Computer Science'),
		('EC' , 'Electronics Engineerning'),
		('MEC' , 'Mechanical Engineering') , 
		('CER' , 'Ceramic Engineering'),
		('CIV' , 'Civil Engineering'),
		('EL','Electrical Engineering'),
		('MnC' , 'Maths and Computing'),
	)
	faculty = models.CharField(max_length = 3 , choices = FACULTY) 
	YEAR = (('1st' , 'First Year'),
		('2nd' , 'Second Year'),
		('3rd', 'Third Year'),
		('4th','Fourth Year'),
		('5th', 'IDD/IMD Fifth Year'),
		('M.Tech 1st' , 'MTech First Year'),
		('M.Tech 2nd' , 'MTech Second Year'),
		('PHD' , 'PHD'),)
	year = models.CharField(max_length = 10 , choices = YEAR)
	DOB = models.DateField('Date of birth' , auto_now=False, auto_now_add=False)
	blood_group_choices =  (('A+' , 'A+'),('B+','B+'),('O+','O+'),('AB+','AB+'),('A-','A-'),('B-','B-'),('O-','O-'),('AB-','AB-'),)
	blood_group = models.CharField(max_length = 3 , choices = blood_group_choices)
	diary_issue_date = models.DateField('Date of issue' , auto_now = True , auto_now_add = False)
	
	current_month = datetime.date.today().month
	current_year = datetime.date.today().year

	if current_month >= 1 and current_month <=6:
		valid_through_year = current_year
	else :
		valid_through_year = current_year + 1

	defaul_validity = str(valid_through_year) + '0630'

	diary_valid_through = models.DateField('Valid through' , default = datetime.datetime.strptime(defaul_validity , "%Y%m%d") , auto_now=False, auto_now_add=False )
	
	phone_number=models.CharField(max_length = 10, validators = [phone_regex] , blank = True)

	def __unicode__(self):              # __unicode__ on Python 2
    		return	self.roll_no



# class Doctor(models.Model):
	
# 	name=models.CharField("Doctor's Name" , max_length = 30)
# 	GENDER=(('M' , 'Male'), ('F' , 'Female') ,)
# 	gender=models.CharField(max_length = 1 , choices = GENDER)
# 	DESIGNATION=(( 'MO', 'Medical Officer'),('CMOH' , 'Chief Medical Officer & Head'),('CMO' , 'Chief Medical Officer') , ('SMO' , 'Senior Medical Officer') , )
# 	designation=models.CharField(max_length = 4 , choices = DESIGNATION)
# 	phone_number=models.CharField(max_length = 10, validators = [phone_regex] , blank = True)
# 	#compounder = models.ForeignKey(SupportStaff , verbose_name = 'Nurse/Compounder')
# 	def __unicode__(self):              # __unicode__ on Python 2
#     		return self.name

# class Bed(models.Model):
# 	BED = (('A' , 'A'),
# 		('B','B'),
# 		('C','C'),
# 	)
# 	bed_type = models.CharField('Type of bed' , max_length=1 , choices = BED)
# 	#lies_in = models.ForeignKey(Room , verbose_name = 'Placed In')
# 	def __unicode__(self):
# 		return str(self.id)

def xray_path(self , filename):
	path = 'xray/%s/%s' %(str(datetime.date.today()) , self.student_id)
	return path

def blood_report_path(self , filename):
	path = 'pathology/%s/%s' %(str(datetime.date.today()) , self.student_id)
	return path

class newEntry(models.Model):
	student_id = models.ForeignKey(Student)
	entry_time = models.DateTimeField('Time of Entry' , auto_now_add = True , auto_now = False)
	updated = models.DateTimeField('Record updated at' , auto_now_add = False , auto_now = True)
	stay_day = models.SmallIntegerField('Stay Duration (Days)' , validators=[MaxValueValidator(15),MinValueValidator(1)], null = True)
	stay_cause = models.CharField('Cause of stay' , max_length = 30 , null = True)
	stay_bed  = models.SmallIntegerField('Bed No.' , validators=[MaxValueValidator(6),MinValueValidator(1)] , null = True)
	blood_test_report = models.FileField(upload_to = blood_report_path , null = True)
	xray_report = models.FileField(upload_to = xray_path , null = True)
	last_updated_by = models.CharField(max_length = 15, blank = True)
	def __unicode__(self):              # __unicode__ on Python 2
    		return str(self.id)


# class user(models.Model):
# 	type_choices = (('R' , 'Receptionist'),('P','Pathology'),('A','Admission'),('X','X-Ray'),)
# 	type_of_user = models.CharField('User Type' , max_length = 1 , choices = type_choices)
# 	user = models.OneToOneField(User)

# class SupportStaff(models.Model):
# 	full_name = models.CharField(max_length = 30)
# 	GENDER = (('M' , 'Male'), 
# 		('F' , 'Female') ,
# 	)
# 	gender = models.CharField(max_length = 1 , choices = GENDER)
# 	DESIGNATION=(( 'N', 'Nurse'),('C' , 'Compounder'),('T' , 'Technician') , ('P' , 'Physiotherapist') , )
# 	designation=models.CharField(max_length = 1 , choices = DESIGNATION)
# 	phone_number=models.CharField(max_length = 10, validators = [phone_regex] , blank = True)
# 	def __unicode__(self):
# 		return str(self.id)

# class Room(models.Model):
# 	CHOICES = [(i,i) for i in range (1,15)]
# 	room_no = models.SmallIntegerField(choices = CHOICES , validators=[
#             MaxValueValidator(15),
#             MinValueValidator(1)
#         ])
# 	def __unicode__(self):
# 		return str(self.room_no)

# class SpecificDiagnosis(models.Model):
# 	name = models.CharField('Name' , max_length = 20 , blank = True)
# 	equipment = models.CharField(max_length = 40 ,primary_key = True)
# 	room_no = models.ForeignKey(Room , verbose_name='Available in Room no.')
# 	supervising_doctor = models.OneToOneField(Doctor , verbose_name = 'Supervising Doctor')
# 	#technician = models.ForeignKey(SupportStaff , verbose_name = 'Technician')
# 	def __unicode__(self):              # __unicode__ on Python 2
#         	return	str(self.equipment)

# class Prescription(models.Model):
# 	new_entry = models.OneToOneField('newEntry' , verbose_name = 'New Entry' , primary_key = True)
# 	medicine_code = models.ForeignKey('Medicine' , verbose_name = 'Medicine Code' , null = False)
# 	dosage = models.CharField('Prescribed Dosage' , max_length = 20)
# 	quantity = models.SmallIntegerField('Quantity of Medicine', validators=[
#             MaxValueValidator(100),
#             MinValueValidator(1)
#         ])
# 	def __unicode__(self):
# 		return str(self.id)


# class Medicine(models.Model):
# 	code = models.CharField('Product Code', max_length = 10 , primary_key = True)
# 	name = models.CharField('Name of Medicine' , max_length = 25)
# 	CATEGORY = (('A' , 'Tablets'),('B' , 'Syrup'),('C', 'Tube/Cream/Ointments'),('D','Drops'),('E','Powder'),)
# 	category = models.CharField(max_length=1 , choices = CATEGORY)
# 	manufacturer = models.CharField('Name of Manufacturer' , max_length = 25)
# 	mfg_data = models.DateField('Manufacture Date', auto_now=False, auto_now_add=False)
# 	expiry_date = models.DateField('Expiry Date' , auto_now=False, auto_now_add=False )
# 	available_no_of_units = models.SmallIntegerField('No. of Units Available', validators=[
#             MaxValueValidator(400),
#             MinValueValidator(1)
#         ])
# 	def __unicode__(self):
# 		return self.code


