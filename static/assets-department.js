function loaddepartment () {
	// body...
	var department_list_api = '/department/api'

	$.get(department_list_api, {}, function(response) {
    response.data.forEach(function(department) {
      var department_item = department.department_name;
      $('.department').prepend('<li>' + department_item + '</li>');
      $('.department-list').prepend('<option value="' + department_item + '">' + department_item + '</option>');
      });
    $('.department-list').chosen();
	});

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

loaddepartment();
$('.department-entry').submit(departmentAdd);