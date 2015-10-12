function onForm(event){
  var d = $('.thesis_proponents').val();
  var data = $(event.target).serializeArray();

  var thesis = {};
  var j = 0;
  for (var i = 0; i < data.length; i++) {
    if (data[i].name == 'thesis_proponents') {
      thesis['thesis_proponent_' + j] = d[j];
      j++;
    } else {thesis[data[i].name] = data[i].value;}
  }

  var thesis_api = '/api/thesis';
  $.post(thesis_api, thesis, function(response) {
    console.log('data', response)
    if (response.status = 'OK') {
       alert('Registration success');
       window.location.replace("/");
     } else {
       alert('Something went wrong');
     }
  });
  return false;
}

function loadAll() {
  var thesis_list_api = '/api/thesis';
  $.get(thesis_list_api, {}, function(response) {
    response.thesis_data.forEach(function(thesis_list) {
      var thesis_item = thesis_list.year + ' ' + thesis_list.title;
      $('.thesis-list').prepend('<li>' + thesis_item + '</li>');
      });

    response.faculty_data.forEach(function(faculty) {
      var thesis_adviser = faculty.full_name;
      $('.thesis_adviser').prepend('<option value="' + thesis_adviser + '">' + thesis_adviser + '</option>');
      $('.faculty-list').append('<li>' + thesis_adviser + '</li>')
    });

    response.student_data.forEach(function(student){
      var thesis_proponent = student.full_name;
      $('.thesis_proponents').prepend('<option value="' + thesis_proponent + '">' + thesis_proponent + '</option>');
    });

    response.university_data.forEach(function(university){
      var thesis_university = university.university_name
      $('.thesis_university').prepend('<option value="' + thesis_university + '">' + thesis_university + '</option>');
    });

    response.college_data.forEach(function(college){
      var thesis_college = college.name
      $('.thesis_college').prepend('<option value="' + thesis_college + '">' + thesis_college + '</option>');
    });

    response.department_data.forEach(function(department){
      var thesis_department = department.name
      $('.thesis_department').prepend('<option value="' + thesis_department + '">' + thesis_department + '</option>');
    });

    $('.thesis_adviser').chosen();
    $('.thesis_proponents').chosen();
    $('.thesis_university').chosen();
    $('.thesis_college').chosen();
    $('.thesis_department').chosen();
  });
}

function onReg(event)
{
  var data = $(event.target).serializeArray();

  var user = {};
  for (var i = 0; i < data.length; i++) {
    user[data[i].name] = data[i].value;
  }

  var user_api = '/register';
  $.post(user_api, user, function(response) {
    console.log('data', response)
    if (response.status = 'OK') {
       alert('Registration success');
       window.location.replace("/");
     } else {
       alert('Something went wrong');
     }
  });
  return false;
}

function facultyAdd(event)
{
  var data = $(event.target).serializeArray();

  var faculty = {};
  for (var i = 0; i < data.length; i++) {
    faculty[data[i].name] = data[i].value;
  }

  var faculty_api = '/faculty/create';
  $.post(faculty_api, faculty, function(response) {
    console.log('data', response)
    if (response.status = 'OK') {
       alert('Registration success');
       window.location.replace("/");
     } else {
       alert('Something went wrong');
     }
  });
  return false;
}

function studentAdd(event)
{
  var data = $(event.target).serializeArray();

  var student = {};
  for (var i = 0; i < data.length; i++) {
    student[data[i].name] = data[i].value;
  }

  var user_api = '/student/create';
  $.post(user_api, student, function(response) {
    console.log('data', response)
    if (response.status = 'OK') {
       alert('Registration success');
       window.location.replace("/");
     } else {
       alert('Something went wrong');
     }
  });
  return false;
}

function universityAdd(event)
{
  var data = $(event.target).serializeArray();

  var university = {};
  for (var i = 0; i < data.length; i++) {
    university[data[i].name] = data[i].value;
  }

  var user_api = '/university/create';
  $.post(user_api, university, function(response) {
    console.log('data', response)
    if (response.status = 'OK') {
       alert('Registration success');
       window.location.replace("/");
     } else {
       alert('Something went wrong');
     }
  });
  return false;
}

function collegeAdd(event)
{
  var data = $(event.target).serializeArray();

  var college = {};
  for (var i = 0; i < data.length; i++) {
    college[data[i].name] = data[i].value;
  }

  var college_api = '/college/create';
  $.post(college_api, college, function(response) {
    console.log('data', response)
    if (response.status = 'OK') {
       alert('Registration success');
       window.location.replace("/");
     } else {
       alert('Something went wrong');
     }
  });
  return false;
}

function departmentAdd(event)
{
  var data = $(event.target).serializeArray();

  var dept = {};
  for (var i = 0; i < data.length; i++) {
    dept[data[i].name] = data[i].value;
  }

  var dept_api = '/department/create';
  $.post(dept_api, dept, function(response) {
    console.log('data', response)
    if (response.status = 'OK') {
       alert('Registration success');
       window.location.replace("/");
     } else {
       alert('Something went wrong');
     }
  });
  return false;
}

loadAll();
$('.thesis-entry').submit(onForm);
$('.regform').submit(onReg);
$('.faculty-entry').submit(facultyAdd);
$('.student-entry').submit(studentAdd);
$('.university-entry').submit(universityAdd);
$('.college-entry').submit(collegeAdd);
$('.department-entry').submit(departmentAdd);
