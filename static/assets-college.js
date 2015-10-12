function loadcollege () {
	// body...
	var college_list_api = '/college/api'

	$.get(college_list_api, {}, function(response) {
    response.data.forEach(function(college) {
      var college_item = college.college_name;
      $('.college').prepend('<li>' +  '<a href="'+ college.id + '">' + college_item + '</a>' + '</li>');
      $('.college-list').prepend('<option value="' + college_item + '">' + college_item + '</option>');
      });
    $('.college-list').chosen();
    $('.college_department').chosen();
	});
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

function collegeEdit(event)
{
  var d = $('.college_department').val();
  var data = $(event.target).serializeArray();

  var college = {};
  var j = 0;
  for (var i = 0; i < data.length; i++) {
    if (data[i].name == 'college_department') {
      college['college_department_' + j] = data[i].value
      j++;
    } else {college[data[i].name] = data[i].value;} 
  }

  var college_api = '/college/' + col_id;
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

var college_list_api = '/college/api'
  var col_id;
  $.get(college_list_api, {}, function(response) {
    response.data.forEach(function(college) {
        col_id = college.id
      });
  });

loadcollege();
$('.college-entry').submit(collegeAdd);
$('.college_departments').submit(collegeEdit);