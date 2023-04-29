

document.getElementById("chance_student").addEventListener('change', function test() {

    var studentId = document.getElementById("chance_student").value;

    temp = fetch('/committee_chancing/load_student_data', {
        method: "POST",    
        body: JSON.stringify({ id: studentId })
      }).then(response=>response.text()).then(input=>{ 

        input = JSON.parse(input);
        
        document.getElementById("student_id").innerHTML = input['id'];
        document.getElementById("start_date").innerHTML = input['start_date'];
        document.getElementById("student_email").innerHTML = input['student_email'];
        document.getElementById("gpa_w").innerHTML = input['gpa_w'];
        
        document.getElementById("package").innerHTML = input['package'];
        document.getElementById("counselor").innerHTML = input['counselor'];
        document.getElementById("high_school").innerHTML = input['high_school'];
        document.getElementById("major_group").innerHTML = input['major_group'];

        document.getElementById("eca_rating").value='0';

        if (input['eca_rating']>0) {
          document.getElementById("eca_rating").value=input['eca_rating'];
        }
        
        document.getElementById("ace_portal_link").innerHTML = "<b><a href='"+input['ace_portal']+"' style=\"text-size:small\">[LINK]</a></b>";
        document.getElementById("google_drive_link").innerHTML = "<b><a href='"+input['google_folder']+"'>[LINK]</a></b>";

        document.getElementById("colleges").innerHTML = " ";
        document.getElementById("save_button").style="height: 30px; background-color: #7e9cff; color: #FFFFFF; width: 200px; text-align: center; padding-top: 3px;border-radius: 5px; display: none"
    })
})


document.getElementById("submit_button").addEventListener('click', function test() {
  var studentId = document.getElementById("chance_student").value;
  var gpaWeighted = document.getElementById("gpa_w").innerHTML;
  var ecaRating = document.getElementById("eca_rating").value;
  var majorGroup = document.getElementById("major_group").innerHTML;

  sendData = {gpa_w: gpaWeighted, id: studentId, eca_rating: ecaRating, major_group: majorGroup}

  temp = JSON.stringify(sendData);

  temp = fetch('/committee_chancing/load_student_colleges', {
      method: "POST",    
      body: temp
    }).then(response=>response.text()).then(input=>{ 
      
      input = JSON.parse(input);

      var output = "<ul id='college_table' class='college_table'>";
      var output = output+"<li id='college_table_header'><div>";
      var output = output+"<div class='college_name_cell' style='padding-top: 10px'><b>College</b></div>";
      var output = output+"<div class='college_chancing_cell'><b>Student Self-Chancing</b></div>";
      var output = output+"<div class='college_chancing_cell'><b>ML<br/>Chancing</b></div>";
      var output = output+"<div class='college_chancing_cell'><b>Committee Chancing</b></div>";
      var output = output+"<div style='clear: both'></div></div></li>"

      

      for (i=0; i<input.length; i++) {

        var setId = input[i][0];
    
        studentChancing = input[i][1];
        mlChancing = input[i][2];
        
        if (studentChancing == ''|| !studentChancing) {studentChancing = '-----'}
        if (mlChancing == '' || !mlChancing) {mlChancing = '-----'}
   
        output = output+"<li><div style='clear:both'>"
        output = output+"<div class='college_name_cell'>"+input[i][0]+"</div>";
        output = output+"<div class='college_chancing_cell'>"+studentChancing+"</div>";
        output = output+"<div class='college_chancing_cell'>"+mlChancing+"</div>";
        
        output = output+"<div class='college_chancing_cell'><select class='committee_chancing standard_select' id='"+setId;
        output = output+"' name='"+setId+"'>";
        
        output = output+"<option value='none' hidden='true'>Select</option>";
        
        if(input[i][3]=='Very Likely') {
          output = output+"<option value='very_likely' selected='true'>Very Likely</option>";
        } else {output = output+"<option value='very_likely'>Very Likely</option>";}  
        
        if(input[i][3]=='Likely') {
          output = output+"<option value='likely' selected='true'>Likely</option>";
        } else {output = output+"<option value='likely'>Likely</option>";}  
        
        if(input[i][3]=='Target') {
          output = output+"<option value='target' selected='true'>Target</option>";
        } else {output = output+"<option value='target'>Target</option>";}  

        if(input[i][3]=='Reach') {
          output = output+"<option value='reach' selected='true'>Reach</option>";
        } else {output = output+"<option value='reach'>Reach</option>";}  

        if(input[i][3]=='Far Reach') {
          output = output+"<option value='far_reach' selected='true'>Far Reach</option>";
        } else {output = output+"<option value='far_reach'>Far Reach</option>";}  

        output = output+"</select>";
        output = output+"</div>";
        output = output+"<div class='college_chancing_cell'><div class='remove_college_button button'><i class='fa fa-minus' aria-hidden='true'></i></div>";
        output = output+"</div>";
        output = output +"</li>"
        
      }

      var output = output+"</ul>"
      

      document.getElementById("addCollegeContainer").style = "display: block";
      document.getElementById("colleges").innerHTML = output;


      $('.remove_college_button').on('click', function(e) {        
        $(this).parent().parent().parent().remove();
        
        var collegeName = $(this).parent().parent().parent().children('div').children('.college_name_cell').text();
        var removeCollege = {'student_id':studentId, 'college_name': collegeName}
        var removeData = JSON.stringify(removeCollege);

        fetch('/committee_chancing/delete_college', {
          method: "POST",    
          body: removeData
        }).then(response=>response.text()).then(input=>{ })        
      })

      $('.committee_chancing').on('change', function(e) {
        
        var studentId = document.getElementById("chance_student").value;
        var sendChancing = '';

        if ($(this).find(":selected").val() == 'very_likely') {sendChancing = 'Very Likely'}
        if ($(this).find(":selected").val() == 'likely') {sendChancing = 'Likely'}
        if ($(this).find(":selected").val() == 'target') {sendChancing = 'Target'}
        if ($(this).find(":selected").val() == 'reach') {sendChancing = 'Reach'}
        if ($(this).find(":selected").val() == 'far_reach') {sendChancing = 'Far Reach'}

        var saveData = {'student_id':studentId, 'college_name': this.id, 'chancing': sendChancing}
        saveData = JSON.stringify(saveData);

        temp = fetch('/committee_chancing/update_chancing', {
          method: "POST",    
          body: saveData
        }).then(response=>response.text()).then(input=>{ })
      

      })
  })

})


document.getElementById("addCollegeButton").addEventListener('click', function test() {
  
  var studentId = document.getElementById("chance_student").value;
  var collegeName = document.getElementById("addCollege").value;
  var newChancing = document.getElementById('newChancing').value;
  var newMLChancing = document.getElementById('new_ml_chancing').innerHTML;
  

  if (newChancing=='very_likely') {newChancing = 'Very Likely'}
  if (newChancing=='likely') {newChancing = 'Likely'}
  if (newChancing=='target') {newChancing = 'Target'}
  if (newChancing=='reach') {newChancing = 'Reach'}
  if (newChancing=='far_reach') {newChancing = 'Far Reach'}

  var newRow = '';
  newRow = newRow+"<li><div style='clear:both'>"
  newRow = newRow+"<div class='college_name_cell'>"+collegeName+"</div>";
  newRow = newRow+"<div class='college_chancing_cell'>"+"-----"+"</div>";
  newRow = newRow+"<div class='college_chancing_cell'>"+newMLChancing+"</div>";

  newRow = newRow+"<div class='college_chancing_cell'><select class='committee_chancing standard_select' id='"+collegeName;
  newRow = newRow+"' name='"+collegeName+"'>";
  
  newRow = newRow+"<option value='none' hidden='true'>Select</option>";

  if(newChancing=='Very Likely') {
    newRow = newRow+"<option value='very_likely' selected='true'>Very Likely</option>";
  } else {newRow = newRow+"<option value='very_likely'>Very Likely</option>";}  
  
  if(newChancing=='Likely') {
    newRow = newRow+"<option value='likely' selected='true'>Likely</option>";
  } else {newRow = newRow+"<option value='likely'>Likely</option>";}  
  
  if(newChancing=='Target') {
    newRow = newRow+"<option value='target' selected='true'>Target</option>";
  } else {newRow = newRow+"<option value='target'>Target</option>";}  

  if(newChancing=='Reach') {
    newRow = newRow+"<option value='reach' selected='true'>Reach</option>";
  } else {newRow = newRow+"<option value='reach'>Reach</option>";}  

  if(newChancing=='Far Reach') {
    newRow = newRow+"<option value='far_reach' selected='true'>Far Reach</option>";
  } else {newRow = newRow+"<option value='far_reach'>Far Reach</option>";}  

  newRow = newRow+"</select>";
  newRow = newRow+"</div>";
  newRow = newRow+"<div class='college_chancing_cell'><div class='remove_college_button button'><i class='fa fa-minus' aria-hidden='true'></i></div>";
  newRow = newRow+"</div>";
  newRow = newRow +"</li>"
  
  $('#college_table').append(newRow);

  var saveData = {'student_id': studentId, 'college_name': collegeName, 'chancing': newChancing}
  saveData = JSON.stringify(saveData);

  temp = fetch('/committee_chancing/update_chancing', {
    method: "POST",    
    body: saveData
  }).then(response=>response.text()).then(input=>{ })


  $('.remove_college_button').on('click', function(e) {        
    $(this).parent().parent().parent().remove();
    
    var collegeName = $(this).parent().parent().parent().children('div').children('.college_name_cell').text();
    var removeCollege = {'student_id':studentId, 'college_name': collegeName}
    var removeData = JSON.stringify(removeCollege);

    fetch('/committee_chancing/delete_college', {
      method: "POST",    
      body: removeData
    }).then(response=>response.text()).then(input=>{ })    
  })

  $('.committee_chancing').on('change', function(e) {
    var studentId = document.getElementById("chance_student").value;
    var sendChancing = '';

    if ($(this).find(":selected").val() == 'very_likely') {sendChancing = 'Very Likely'}
    if ($(this).find(":selected").val() == 'likely') {sendChancing = 'Likely'}
    if ($(this).find(":selected").val() == 'target') {sendChancing = 'Target'}
    if ($(this).find(":selected").val() == 'reach') {sendChancing = 'Reach'}
    if ($(this).find(":selected").val() == 'far_reach') {sendChancing = 'Far Reach'}

    var saveData = {'student_id':studentId, 'college_name': this.id, 'chancing': sendChancing}
    saveData = JSON.stringify(saveData);

    temp = fetch('/committee_chancing/update_chancing', {
      method: "POST",    
      body: saveData
    }).then(response=>response.text()).then(input=>{ })
  })
})

document.getElementById("addCollege").addEventListener('change', function test() {

  var studentId = document.getElementById("chance_student").value;
  var gpaWeighted = document.getElementById("gpa_w").innerHTML;
  var ecaRating = document.getElementById("eca_rating").value;
  var majorGroup = document.getElementById("major_group").innerHTML;
  var collegeName = document.getElementById("addCollege").value;

  var chanceData = {
    'student_id': studentId, 
    'college_name': collegeName, 
    'gpa_weighted': gpaWeighted,
    'eca_rating': ecaRating,
    'major_group': majorGroup
  }

  var chanceData = JSON.stringify(chanceData)

  fetch('/committee_chancing/quick_ml_chancing', {
    method: "POST",    
    body: chanceData
  }).then(response=>response.text()).then(input=>{

    input = JSON.parse(input);
    document.getElementById("new_ml_chancing").innerHTML=input['ml_chancing']
    //$('new_ml_chancing').text('hi');

  })


})