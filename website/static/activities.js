
function deleteCAActivity(activityId) {
  fetch('/delete-ca_activity', {
    method: "POST",
    body: JSON.stringify({ activityId: activityId }),
  }).then((_res) => {
    window.location.href = '/activities';
  });
}

$('.form-select').change(function() {
  $(this).parent().parent().children('div').children('.save-button').css('background-color', '#007bff'); 
})

$('textarea').keyup(function() {
  
  var characterCount = $(this).val().length,
      current = $(this).parent().children('div').children('.current');
      maximum = $(this).parent().children('div').children('.maximum');
      theCount = $('#the-count');
    
  current.text(characterCount);
 
  if (characterCount <= maximum.text()) {
    current.css('color', '#000000');
  }
  if (characterCount > maximum.text()) {
    current.css('color', '#FF0000');
    theCount.css('font-weight','normal');
  } else {
    maximum.css('color','#000000');
    theCount.css('font-weight','normal');
  } 

  $(this).parents('#activity-form').find('.save-button').css('background-color', '#007bff');
  
});

$('.reorder-button-down').click(function() {
  b = $(this).parents('#activity-form').find('.form-contents');
  a = $(this).parents('#activity-form').parent().nextAll().eq(0).find('.form-contents');

  
  var tmp = $('<span>').hide();

  a.before(tmp);
  b.before(a);
  tmp.replaceWith(b);

  saveData($(this).parents('#activity-form'));
  saveData($(this).parents('#activity-form').parent().nextAll().eq(0).find('#activity-form'));  
})


$('.reorder-button-up').click(function() {
  b = $(this).parents('#activity-form').find('.form-contents');
  a = $(this).parents('#activity-form').parent().prevAll().eq(0).find('.form-contents');

  
  var tmp = $('<span>').hide();

  a.before(tmp);
  b.before(a);
  tmp.replaceWith(b);

  saveData($(this).parents('#activity-form'));
  saveData($(this).parents('#activity-form').parent().prevAll().eq(0).find('#activity-form'));  
})

function saveData (inputForm) {
  
  var unindexed_array = inputForm.serializeArray();
  var indexed_array = {};

  $.map(unindexed_array, function(n, i){
      indexed_array[n['name']] = n['value'];
  });
    

  if(indexed_array['action'] == 'update') {    
    data = JSON.stringify(indexed_array);
    fetch('/activities', {
      method: "POST",    
      body: data
    });
  }

}


$('form').on( 'submit', function(e) {
  
  var unindexed_array = $(this).serializeArray();
  var indexed_array = {};

  $.map(unindexed_array, function(n, i){
      indexed_array[n['name']] = n['value'];
  });

  temp = JSON.stringify(indexed_array)
  alert(temp)

  if(indexed_array['action'] == 'update') {
    e.preventDefault();
    data = JSON.stringify(indexed_array);

    fetch('/activities', {
      method: "POST",    
      body: data
    }).then((_res) => {      
      $(this).children('div').children('.save-button').css('background-color', '#6c757d');
      $(this).parent().css('background-color','rgb(215, 215, 215)')
    });
  }

})