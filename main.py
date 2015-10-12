import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json
import csv

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class thesisentry(ndb.Model):
	thesis_year = ndb.StringProperty()
	thesis_title = ndb.StringProperty(indexed=True)
	thesis_abstract = ndb.TextProperty()
	thesis_adviser = ndb.KeyProperty(kind='Faculty',indexed=True)
	thesis_section = ndb.StringProperty()
	thesis_department = ndb.KeyProperty(kind='Department',indexed=True)
	thesis_proponent = ndb.KeyProperty(kind='Student', repeated=True)

	thesis_author = ndb.KeyProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_by_name(model, name):
		try:
			student = model.query(model.thesis_title == name)
			return student.get()
		except Exception:
			return None

class User(ndb.Model):
	email = ndb.StringProperty(indexed=True)
	first_name = ndb.StringProperty()
	last_name = ndb.StringProperty()
	phone_number = ndb.IntegerProperty()
	created_date = ndb.DateTimeProperty(auto_now_add=True)

class Faculty(ndb.Model):
	faculty_title = ndb.StringProperty(indexed=True)
	faculty_fname = ndb.StringProperty(indexed=True)
	faculty_sname = ndb.StringProperty(indexed=True)
	faculty_full = ndb.StringProperty(indexed=True)
	faculty_email = ndb.StringProperty(indexed=True)
	faculty_phone = ndb.StringProperty(indexed=True)
	faculty_bday = ndb.StringProperty(indexed=True)
	faculty_department = ndb.KeyProperty(kind='Department', indexed=True)
	created_date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_by_name(model, name):
		try:
			adviser = model.query(model.faculty_full == name)
			return adviser.get()
		except Exception:
			return None

class Student(ndb.Model):
	student_fname = ndb.StringProperty(indexed=True)
	student_sname = ndb.StringProperty(indexed=True)
	student_full = ndb.StringProperty(indexed=True)
	student_email = ndb.StringProperty(indexed=True)
	student_phone = ndb.StringProperty(indexed=True)
	student_number = ndb.StringProperty(indexed=True)
	student_graduated = ndb.IntegerProperty(indexed=True)
	student_bday = ndb.StringProperty(indexed=True)
	student_department = ndb.KeyProperty(kind='Department', indexed=True)
	created_date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_by_name(model, name):
		try:
			student = model.query(model.student_full == name)
			return student.get()
		except Exception:
			return None

class University(ndb.Model):
	university_name = ndb.StringProperty(indexed=True)
	university_initial = ndb.StringProperty(indexed=True)
	university_address = ndb.StringProperty(indexed=True)
	created_date = ndb.DateTimeProperty(auto_now_add=True)

class Department(ndb.Model):
	department_college = ndb.KeyProperty(kind='College', indexed=True)
	department_name = ndb.StringProperty(indexed=True)
	department_chair = ndb.KeyProperty(kind='Faculty',indexed=True)
	created_date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_by_name(model, name):
		try:
			department = model.query(model.department_name == name)
			return department.get()
		except Exception:
			return None

class College(ndb.Model):
	college_university = ndb.KeyProperty(kind='University',indexed=True)
	college_name = ndb.StringProperty(indexed=True)
	college_departments = ndb.KeyProperty(repeated=True)
	created_date = ndb.DateTimeProperty(auto_now_add=True)
						
class MainPageHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				link_text = 'Logout'
				template_values = {
					'thesis_create_url': '/thesis/create',
					'faculty_create_url': '/faculty/create',
					'student_create_url': '/student/create',
					'university_create_url': '/university/create',
					'college_create_url': '/college/create',
					'department_create_url': '/department/create',
					'faculty_view_url': '/faculty/list',
					'student_view_url':'/student/list',
					'university_list_url':'/university/list',
					'college_list_url': '/college/list',
					'logout_url': users.create_logout_url('/'),
					'user': user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/main.html')
				self.response.write(template.render(template_values))
			else:
				self.redirect('/register')

		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))

class APIHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				thesisdet = thesisentry.query().order(-thesisentry.date).fetch()
				thesis_list = []
				for thesis in thesisdet:
					# user = User.query(User.key == thesis.thesis_author)
					e = []
					# for u in user:
					# 	e.append({
					# 		'first_name':u.first_name,
					# 		'last_name':u.last_name
					# 	})

					departmentlist = Department.query(Department.key == thesis.thesis_department)
					d = []
					for de in departmentlist:
						d.append({
							'name':de.department_name
							})

					facultylist = Faculty.query(Faculty.key == thesis.thesis_adviser)
					f = []
					for fa in facultylist:
						f.append({
							'name':fa.faculty_full
							})

					thesis_list.append({
						'id' : thesis.key.urlsafe(),
						'year': thesis.thesis_year,
						'title': thesis.thesis_title,
						'abstract': thesis.thesis_abstract,
						'adviser': f,
						'section': thesis.thesis_section,
						'department': d,
						'author': e,
						'thesis_id': thesis.key.id()

					})


				response = {
					'result' : 'OK',
					'thesis_data' : thesis_list
				}
				self.response.headers['Content-Type'] = 'application.json'
				self.response.out.write(json.dumps(response))

			else:
				self.redirect('/register')

		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))		

	def post(self):
		thesis = thesisentry()
		user = User()
		faculty = Faculty()

		loggedin_user = users.get_current_user()
		user_key = ndb.Key('User', loggedin_user.user_id())

		thesis_proponents = []
		i = 0
		while self.request.get('thesis_proponent_' + str(i)) is not None and self.request.get('thesis_proponent_' + str(i)) != '':
			thesis_proponent_temp = Student.query(Student.student_full == self.request.get('thesis_proponent_' + str(i)))
			if thesis_proponent_temp.count():
				thesis_proponent_temp = thesis_proponent_temp.get()
				thesis_proponents.append(thesis_proponent_temp.key)
			else:
				thesis_proponent_temp = Faculty.query(Faculty.faculty_full == self.request.get('thesis_proponent_' + str(i)))
				if thesis_proponent_temp.count():
					thesis_proponent_temp = thesis_proponent_temp.get()
					thesis_proponents.append(thesis_proponent_temp.key)
				else:
					thesis_proponents.append(None)
			i += 1

		logging.info(thesis_proponents)

		thesis_adviser_temp = Faculty.query(Faculty.faculty_full == self.request.get('thesis_adviser'))
		thesis_adviser_temp = thesis_adviser_temp.get()
		thesis_adviser_key = thesis_adviser_temp.key

		thesis_department_temp = Department.query(Department.department_name == self.request.get('thesis_department'))
		thesis_department_temp = thesis_department_temp.get()
		thesis_department_key = thesis_department_temp.key

		thesis.thesis_author = user_key
		thesis.thesis_year = self.request.get('thesis_year')
		thesis.thesis_title = self.request.get('thesis_title')
		thesis.thesis_abstract = self.request.get('thesis_abstract')
		thesis.thesis_adviser = ndb.Key('Faculty', thesis_adviser_key.id())
		thesis.thesis_section = self.request.get('thesis_section')
		thesis.thesis_proponent = thesis_proponents
		thesis.thesis_department = ndb.Key('Department', thesis_department_key.id())

		thesis.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result': 'OK',
			'data': {
				'id' : thesis.key.urlsafe(),
				'year': thesis.thesis_year,
				'title': thesis.thesis_title,
				'abstract': thesis.thesis_abstract,
				'section': thesis.thesis_section,
				'author': user_key.get().first_name + ' ' + user_key.get().last_name
			}
		}
		self.response.out.write(json.dumps(response))

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			user_key = ndb.Key('User', user.user_id())
			user_info = user_key.get()
			if user_info:
				self.redirect('/home')
			else:
				self.redirect('/register')

class RegistrationHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get()
			if user:
				self.redirect('/home')
			else:
				template_data = {
					'email':loggedin_user.email()
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/register.html')
				self.response.write(template.render(template_data))
		else:
			self.redirect(users.create_login_url('/register'))

	def post(self):
		user = User(id=users.get_current_user().user_id())
		user.phone_number = int(self.request.get('phone_number'))
		user.email = self.request.get('email')
		user.first_name = self.request.get('first_name')
		user.last_name = self.request.get('last_name')
		user.put()
		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result':'OK',
			'data':{
				'first_name':user.first_name,
				'last_name':user.last_name,
				'phone_number':user.phone_number,
				'id':users.get_current_user().user_id()
			}
		}
		self.response.out.write(json.dumps(response))

class ThesisPageHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				template_values = {
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/thesis.html')
				self.response.write(template.render(template_values))

			else:
				self.redirect('/register')

		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))

class FacultyHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				template_values = {
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/faculty.html')
				self.response.write(template.render(template_values))
			else:
				self.redirect('/register')

		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))

	def post(self):
		faculty = Faculty()

		faculty_department_temp = Department.query(Department.department_name == self.request.get('faculty_department'))
		faculty_department_temp = faculty_department_temp.get()
		faculty_department_key = faculty_department_temp.key

		faculty.faculty_title = self.request.get('faculty_title')
		faculty.faculty_fname = self.request.get('faculty_fname')
		faculty.faculty_sname = self.request.get('faculty_sname')
		faculty_full = faculty.faculty_fname + ' ' + faculty.faculty_sname
		faculty.faculty_full = faculty_full
		faculty.faculty_email = self.request.get('faculty_email')
		faculty.faculty_phone = self.request.get('faculty_phone')
		faculty.faculty_department = ndb.Key('Department', faculty_department_key.id())
		faculty.faculty_bday = self.request.get('faculty_bday')
		faculty.key = ndb.Key(Faculty, faculty_full.strip().replace(' ', '').replace('.','').replace(',','').lower())
		faculty.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result':'OK',
			'data':{
				'title':faculty.faculty_title,
				'first_name':faculty.faculty_fname,
				'last_name':faculty.faculty_sname,
				'full_name':faculty.faculty_full,
				'email':faculty.faculty_email,
				'phone':faculty.faculty_phone,
				'bday':faculty.faculty_bday
			}
		}
		self.response.out.write(json.dumps(response))

class StudentHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				template_values = {
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/student.html')
				self.response.write(template.render(template_values))
			else:
				self.redirect('/register')

	def post(self):
		student = Student()

		student_department_temp = Department.query(Department.department_name == self.request.get('student_department'))
		student_department_temp = student_department_temp.get()
		student_department_key = student_department_temp.key

		student.student_fname = self.request.get('student_fname')
		student.student_sname = self.request.get('student_sname')
		student.student_full = student.student_fname + ' ' + student.student_sname
		student.student_phone = self.request.get('student_phone')
		student.student_email = self.request.get('student_email')
		student.student_number = self.request.get('student_number')
		student.student_graduated = int(self.request.get('student_graduated'))
		student.student_department = ndb.Key('Department', student_department_key.id())
		student.student_bday = self.request.get('student_bday')
		student.key = ndb.Key(Student, student.student_full.strip().replace(' ', '').replace('.','').replace(',','').lower())
		student.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result':'OK',
			'data':{
				'first_name':student.student_fname,
				'last_name':student.student_sname,
				'full_name':student.student_full,
				'phone':student.student_phone,
				'email':student.student_email,
				'student_number':student.student_number,
				'year_graduated':student.student_graduated
			}
		}
		self.response.out.write(json.dumps(response))

class UniversityHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				template_values = {
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/university.html')
				self.response.write(template.render(template_values))
			else:
				self.redirect('/register')

	def post(self):
		university = University()

		university.university_name = self.request.get('university_name')
		university.university_initial = self.request.get('university_initial')
		university.university_address = self.request.get('university_address')
		university.key = ndb.Key(University, university.university_initial.strip().replace(' ', '').replace('.','').replace(',','').lower())
		university.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result':'OK',
			'data':{
				'university_name': university.university_name,
				'university_initial': university.university_initial,
				'university_address': university.university_address
			}
		}

		self.response.out.write(json.dumps(response))

class CollegeHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				template_values = {
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/college.html')
				self.response.write(template.render(template_values))
			else:
				self.redirect('/register')

	def post(self):
		college = College()
		
		college_university_temp = University.query(University.university_name == self.request.get('college_university'))
		college_university_temp = college_university_temp.get()
		college_university_key = college_university_temp.key

		college.college_university = ndb.Key('University', college_university_key.id())
		college.college_name = self.request.get('college_name')
		college.key = ndb.Key(College, college.college_name.strip().replace(' ', '').replace('.','').replace(',','').lower())
		college.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result':'OK',
			'data':{
				'college_name': college.college_name
			}
		}
		self.response.out.write(json.dumps(response))

class DepartmentHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				template_values = {
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/department.html')
				self.response.write(template.render(template_values))
			else:
				self.redirect('/register')

	def post(self):
		department = Department()

		department_college_temp = College.query(College.college_name == self.request.get('department_college'))
		department_college_temp = department_college_temp.get()
		department_college_key = department_college_temp.key

		department_chair_temp = Faculty.query(Faculty.faculty_full == self.request.get('department_chair'))
		department_chair_temp = department_chair_temp.get()
		department_chair_key = department_chair_temp.key
		
		department.department_college = ndb.Key('College', department_college_key.id())
		department.department_name = self.request.get('department_name')
		department.department_chair = ndb.Key('Faculty', department_chair_key.id())

		department.key = ndb.Key(Department, department.department_name.strip().replace(' ', '').replace('.','').replace(',','').lower())
		department.put()

		college = College.query(College.key == department.department_college)
		c = college.get()
		logging.info(c)
		collegelist = []
		collegelist = c.college_departments
		logging.info(collegelist)
		collegelist.append(department.key)
		c.college_departments = collegelist
		c.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result':'OK',
			'data':{
				'department_name': department.department_name
			}
		}
		self.response.out.write(json.dumps(response))

class DataImportHandler(webapp2.RequestHandler):
	def get(self):
		script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
		script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
		rel_path = "data/data.csv"
		abs_file_path = os.path.join(script_dir, rel_path)
		filepath = open(abs_file_path)
		file = csv.reader(filepath)
		i = 0
		for f in file:
			thesis_title = f[4]
			test = thesisentry.get_by_name(thesis_title)

			if test is None:
				thesis = thesisentry()
				thesis.thesis_year = f[3]
				thesis.thesis_title = f[4]
				thesis.thesis_abstract = f[5]
				thesis.thesis_section = f[6]
				adviser_keyname = f[7].strip().replace(' ', '').replace('.','').replace(',','').lower()
				adviser_name = f[7]
				thesis_adviser = Faculty.get_by_name(adviser_name)

				if thesis_adviser is None:
					thesis_adviser = Faculty(key=ndb.Key(Faculty, adviser_keyname), faculty_full=f[7])
					thesis_adviser.put()
				thesis.thesis_adviser = thesis_adviser.key

				department_name = f[2]
				thesis_department = Department.get_by_name(department_name)

				if thesis_department is None:
					thesis_department = Department(department_name=department_name)
					thesis_department.put()
				thesis.thesis_department = thesis_department.key
				

				proponent = []

				for i in range(8, 12):
					if len(f[i]) is not 0:
						proponent.append(f[i])
				proponent_list = []
				for p in proponent:
					thesis_proponent = Student.get_by_name(p)
					if thesis_proponent is None:
						thesis_proponent = Student(key=ndb.Key(Student, p.strip().replace(' ','').replace('.','').replace(',','').lower()), student_full=p)
						thesis_proponent.put()
					proponent_list.append(thesis_proponent.key)
				thesis.thesis_proponent = proponent_list
				thesis.put()
			i += 1
			logging.info(i)
		filepath.close()

class SetupHandler(webapp2.RequestHandler):
	def get(self):
		fname = 'Pedrito '
		sname = 'Tenerife, Jr.'
		title = 'Engr. '
		fullname = (fname + sname).strip().replace(' ','').replace('.','').replace(',','').lower()
		chairperson = Faculty(key=ndb.Key(Faculty, fullname), faculty_fname=fname, faculty_sname=sname, faculty_title=title, faculty_full=title + fname + sname, faculty_email='pmtenerife@pup.edu.ph')
		chairperson.put()
		logging.info(chairperson.key.id())

		university = University(key=ndb.Key(University, 'pup'), university_name='Polytechnic University of the Philippines',university_address='Sta. Mesa, Manila',university_initial='PUP')
		university.put()

		college = College(key=ndb.Key(College, 'engineering'), college_name='Engineering', college_university=university.key)
		college.put()

		department = Department(key=ndb.Key(Department, 'coe'), department_name='COE', department_college=college.key, department_chair=chairperson.key)
		department.put()

		dept = []
		dept.append(department.key)
		college.college_departments = dept
		college.put()

		chairperson.faculty_department = department.key
		chairperson.put()

class FacultyListHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				template_values = {
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/facultylist.html')
				self.response.write(template.render(template_values))

			else:
				self.redirect('/register')
		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))

	def post(self):
		faculty = Faculty()

		faculty_department_temp = Department.query(Department.department_name == self.request.get('faculty_department'))
		faculty_department_temp = faculty_department_temp.get()
		faculty_department_key = faculty_department_temp.key

		faculty.faculty_title = self.request.get('faculty_title')
		faculty.faculty_fname = self.request.get('faculty_fname')
		faculty.faculty_sname = self.request.get('faculty_sname')
		faculty_full = faculty.faculty_fname + ' ' + faculty.faculty_sname
		faculty.faculty_full = faculty_full
		faculty.faculty_email = self.request.get('faculty_email')
		faculty.faculty_phone = self.request.get('faculty_phone')
		faculty.faculty_department = ndb.Key('Department', faculty_department_key.id())
		faculty.faculty_bday = self.request.get('faculty_bday')
		faculty.key = ndb.Key(Faculty, faculty_full.strip().replace(' ', '').replace('.','').replace(',','').lower())
		faculty.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result':'OK',
			'data':{
				'title':faculty.faculty_title,
				'first_name':faculty.faculty_fname,
				'last_name':faculty.faculty_sname,
				'full_name':faculty.faculty_full,
				'email':faculty.faculty_email,
				'phone':faculty.faculty_phone,
				'bday':faculty.faculty_bday
			}
		}
		self.response.out.write(json.dumps(response))

class FacultyAPIHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				facultylist = Faculty.query().order(Faculty.created_date).fetch()
				faculty = []
				for f in facultylist:
					faculty.append({
						'id':f.key.id(),
						'title':f.faculty_title,
						'first_name':f.faculty_fname,
						'last_name':f.faculty_sname,
						'full_name':f.faculty_full,
						'email':f.faculty_email,
						'phone':f.faculty_phone
						})
				response = {
					'result' : 'OK',
					'faculty_data': faculty
				}
				self.response.headers['Content-Type'] = 'application.json'
				self.response.out.write(json.dumps(response))
	
class ThesisCreateAPI(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				facultylist = Faculty.query().order(Faculty.created_date).fetch()
				faculty = []
				for f in facultylist:
					faculty.append({
						'title':f.faculty_title,
						'first_name':f.faculty_fname,
						'last_name':f.faculty_sname,
						'full_name':f.faculty_full,
						'email':f.faculty_email,
						'phone':f.faculty_phone
						})

				studentlist = Student.query().order(Student.created_date).fetch()
				student = []
				for s in studentlist:
					student.append({
						'first_name':s.student_fname,
						'last_name':s.student_sname,
						'full_name':s.student_full,
						'phone':s.student_phone,
						'email':s.student_email,
						'student_number':s.student_number,
						'year_graduated':s.student_graduated
						})

				departmentlist = Department.query().order(Department.created_date).fetch()
				department = []
				for d in departmentlist:
					col = College.query(College.key == d.department_college)
					c = []
					for co in col:
						c.append({
							'name':co.college_name
							})
					department.append({
						'college':c,
						'name':d.department_name
						})	

				response = {
					'result' : 'OK',
					'faculty_data': faculty,
					'student_data': student,
					'department_data':department
				}
				self.response.headers['Content-Type'] = 'application.json'
				self.response.out.write(json.dumps(response))

class StudentsAPIHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				studentlist = Student.query().order(Student.created_date).fetch()
				student = []
				for s in studentlist:
					student.append({
						'id': s.key.id(),
						'first_name':s.student_fname,
						'last_name':s.student_sname,
						'full_name':s.student_full,
						'phone':s.student_phone,
						'email':s.student_email,
						'student_number':s.student_number,
						'year_graduated':s.student_graduated

						})
				response = {
					'result' : 'OK',
					'data': student
				}
				self.response.headers['Content-Type'] = 'application.json'
				self.response.out.write(json.dumps(response))

class StudentListHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				template_values = {
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/studentlist.html')
				self.response.write(template.render(template_values))

			else:
				self.redirect('/register')
		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))

class UniversityAPIHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				universitylist = University.query().order(University.created_date).fetch()
				university = []
				for u in universitylist:
					university.append({
						'id': u.key.id(),
						'university_name': u.university_name,
						'university_initial': u.university_initial,
						'university_address': u.university_address

						})
				response = {
					'result' : 'OK',
					'data': university
				}
				self.response.headers['Content-Type'] = 'application.json'
				self.response.out.write(json.dumps(response))

class UniversityListHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				template_values = {
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/universitylist.html')
				self.response.write(template.render(template_values))

			else:
				self.redirect('/register')
		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))

class CollegeAPIHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				collegelist = College.query().order(College.created_date).fetch()
				college = []
				for c in collegelist:
					un = University.query(University.key == c.college_university)
					un = un.get()

					college.append({
						'id' : c.key.id(),
						'college_name': c.college_name,
						'college_university': un.university_name
						})
				response = {
					'result' : 'OK',
					'data': college
				}
				self.response.headers['Content-Type'] = 'application.json'
				self.response.out.write(json.dumps(response))

class CollegeListHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				template_values = {
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/collegelist.html')
				self.response.write(template.render(template_values))

			else:
				self.redirect('/register')
		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))

class DepartmentAPIHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				departmentlist = Department.query().order(Department.created_date).fetch()
				dept = []
				for d in departmentlist:
					c = College.query(College.key == d.department_college)
					c = c.get()

					f = Faculty.query(Faculty.key == d.department_chair)
					f = f.get()

					dept.append({
						'department_name': d.department_name,
						'department_college': c.college_name,
						'department_chair': f.faculty_full
						})
				response = {
					'result' : 'OK',
					'data': dept
				}
				self.response.headers['Content-Type'] = 'application.json'
				self.response.out.write(json.dumps(response))

class FacultyEditHandler(webapp2.RequestHandler):
	def get(self, id):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				faculty = Faculty.get_by_id(id)
				department = None
				if faculty.faculty_department is not None:
					department = Department.query(Department.key == faculty.faculty_department)
					department = department.get()
					department = department.department_name
				data = {
					'item' : faculty,
					'dept' : department,
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/facultyedit.html')
				self.response.write(template.render(data))

			else:
				self.redirect('/register')
		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))

class StudentEdithandler(webapp2.RequestHandler):
	def get(self, id):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				student = Student.get_by_id(id)
				department = None

				if student.student_department is not None:
					department = Department.query(Department.key == student.student_department)
					department = department.get()
					department = department.department_name
				data = {
					'item' : student,
					'dept' : department,
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/studentedit.html')
				self.response.write(template.render(data))

			else:
				self.redirect('/register')
		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))

class UniversityEditHandler(webapp2.RequestHandler):
	def get(self, id):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				university = University.get_by_id(id)

				data = {
					'item' : university,
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('/pages/universityedit.html')
				self.response.write(template.render(data))

			else:
				self.redirect('/register')
		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))

class CollegeEditHandler(webapp2.RequestHandler):
	def get(self, id):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				college = College.get_by_id(id)

				depts = []
				for c in college.college_departments:
					department = Department.query(Department.key == c)
					department = department.get()
					depts.append(department.department_name)

				university = University.query(University.key == college.college_university)
				university = university.get()


				data = {
					'item' : college,
					'univ' : university.university_name,
					'dept' : depts,
					'logout_url':logout_url,
					'user':user
				}

				for i in range(0, len(depts)):
					data['college_dept_' + str(i)] = depts[i]

				logging.info(data)

				template = JINJA_ENVIRONMENT.get_template('/pages/collegeedit.html')
				self.response.write(template.render(data))

			else:
				self.redirect('/register')
		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))

	def post(self, id):
		college = College()
		
		college_university_temp = University.query(University.university_name == self.request.get('college_university'))
		college_university_temp = college_university_temp.get()
		college_university_key = college_university_temp.key

		department = college.college_departments

		dept_temp = []
		i = 0
		while self.request.get('college_department_' + str(i)) is not None and self.request.get('college_department_' + str(i)) != '':
			college_dept_temp = Department.query(Department.department_name == self.request.get('college_department_' + str(i)))
			college_dept_temp = college_dept_temp.get()
			if college_dept_temp.key not in department:
				department.append(college_dept_temp.key)
			i += 1

		college.college_university = ndb.Key('University', college_university_key.id())
		college.college_name = self.request.get('college_name')
		college.college_departments = department
		college.key = ndb.Key(College, college.college_name.strip().replace(' ', '').replace('.','').replace(',','').lower())
		college.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result':'OK',
			'data':{
				'college_name': college.college_name
			}
		}
		self.response.out.write(json.dumps(response))



app = webapp2.WSGIApplication([
	('/api/thesis', APIHandler),
	('/register', RegistrationHandler),
	('/login', LoginHandler),
	('/home', MainPageHandler),
	('/thesis/create', ThesisPageHandler),
	('/faculty/create', FacultyHandler),
	('/student/create', StudentHandler),
	('/university/create', UniversityHandler),
	('/college/create', CollegeHandler),
	('/department/create', DepartmentHandler),
	('/data/import', DataImportHandler),
	('/setup', SetupHandler),
	('/faculty/list', FacultyListHandler),
	('/faculty/api', FacultyAPIHandler),
	('/thesis/create/api', ThesisCreateAPI),
	('/student/api', StudentsAPIHandler),
	('/student/list', StudentListHandler),
	('/university/api', UniversityAPIHandler),
	('/university/list', UniversityListHandler),
	('/college/api', CollegeAPIHandler),
	('/college/list', CollegeListHandler),
	('/department/api', DepartmentAPIHandler),
	('/faculty/(.*)', FacultyEditHandler),
	('/student/(.*)', StudentEdithandler),
	('/university/(.*)', UniversityEditHandler),
	('/college/(.*)', CollegeEditHandler),
	('/', MainPageHandler)
], debug=True)
