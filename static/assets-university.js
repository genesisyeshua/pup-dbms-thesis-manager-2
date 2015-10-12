function loaduniversity () {
	// body...
	var university_list_api = '/university/api'

	$.get(university_list_api, {}, function(response) {
    response.data.forEach(function(university) {
      var university_item = university.university_name;
      $('.university').prepend('<li>' + '<a href="' + university.id + '">' + university_item + '</a>' + '</li>');
      $('.university-list').prepend('<option value="' + university_item + '">' + university_item + '</option>');
      });
    $('.university-list').chosen();
	});
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

loaduniversity();
$('.university-entry').submit(universityAdd);