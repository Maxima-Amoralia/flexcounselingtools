$('#counselors').on('change', function(e) {
  
  selectedCounselor = $(this).find(":selected").val();

  var sendData = {'counselor':selectedCounselor}
  sendData = JSON.stringify(sendData);

  temp = fetch('/counselor_chancing/load_counselor', {
    method: "POST",    
    body: sendData
  }).then(response=>response.text()).then(input=>{
    input = JSON.parse(input);
    alert(input);

  })
})

$("#addCollege").on('change', function test() {

  var studentId = document.getElementById("student_id").value;
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
    $('#new_ml_chancing').html(input['ml_chancing']);

  })

})



$('.student').on('click', function(e) {

  var studentId = $(this).attr('id');

  returnedData = fetch('/counselor_chancing/load_student_data', {
    method: "POST",    
    body: JSON.stringify({ id: studentId })
  }).then(response=>response.text()).then(input=>{
      
    alert(input)
      input = JSON.parse(input);
      
      document.getElementById("student_list").style.display="none";
      document.getElementById("studentInfo").style.display ="block";
      document.getElementById("colleges").style.display ="block";


      document.getElementById("student_id").innerHTML = input['id'];
      document.getElementById("start_date").innerHTML = input['start_date'];
      document.getElementById("student_email").innerHTML = input['student_email'];
      document.getElementById("gpa_w").innerHTML = input['gpa_w'];
      
      document.getElementById("package").innerHTML = input['package'];
      document.getElementById("counselor").innerHTML = input['counselor'];
      document.getElementById("high_school").innerHTML = input['high_school'];
      document.getElementById("major_group").innerHTML = input['major_group'];

      document.getElementById("ace_portal_link").innerHTML = '<a href='+input['ace_portal']+'>ACE Portal Profile</a>';
      document.getElementById("google_drive_link").innerHTML = '<a href='+input['google_folder']+'>Google Folder</a>';

      

      var output = "<ul id='college_table' class='college_table'>";
      var output = output+"<li id='college_table_header'><div>";
      var output = output+"<div class='college_name_header' style='padding-top: 10px'><b>College</b></div>";
      var output = output+"<div class='college_chancing_header'><b>Student<br/>Chancing</b></div>";
      var output = output+"<div class='college_chancing_header'><b>ML<br/>Chancing</b></div>";
      var output = output+"<div class='college_chancing_header'><b>Committee<br/>Chancing</b></div>";
      var output = output+"<div class='college_chancing_header'><b>Counselor<br/>Chancing</b></div>";
      var output = output+"<div class='college_chancing_header'><b>Counselor<br/>Recs</b></div>";
      var output = output+"<div style='clear: both'></div></div></li>"      


      for (i=0; i<input.colleges.length; i++) {

        var setId = input.colleges[i][0];
    
        studentChancing = input.colleges[i][1];
        mlChancing = input.colleges[i][2];
        committeeChancing = input.colleges[i][3];
        counselorChancing = input.colleges[i][4];
        counselorRec = input.colleges[i][5];

        if (studentChancing == ''|| !studentChancing) {studentChancing = '-----'}
        if (mlChancing == '' || !mlChancing) {mlChancing = '-----'}
   
        output = output+"<li><div style='clear:both'>"
        output = output+"<div class='college_name_cell'>"+input.colleges[i][0]+"</div>";
        output = output+"<div class='college_chancing_cell'>"+studentChancing+"</div>";
        output = output+"<div class='college_chancing_cell'>"+mlChancing+"</div>";
        output = output+"<div class='college_chancing_cell'>"+committeeChancing+"</div>";
        output = output+"<div class='college_chancing_cell'><select class='counselor_chancing standard_select' id='"+setId;
        output = output+"' name='"+setId+"'>";
        
        output = output+"<option value='none' hidden='true'>Select</option>";

        if(counselorChancing=='Very Likely') {
          output = output+"<option value='very_likely' selected='true'>Very Likely</option>";
        } else {output = output+"<option value='very_likely'>Very Likely</option>";}  
        
        if(counselorChancing=='Likely') {
          output = output+"<option value='likely' selected='true'>Likely</option>";
        } else {output = output+"<option value='likely'>Likely</option>";}  
        
        if(counselorChancing=='Target') {
          output = output+"<option value='target' selected='true'>Target</option>";
        } else {output = output+"<option value='target'>Target</option>";}  

        if(counselorChancing=='Reach') {
          output = output+"<option value='reach' selected='true'>Reach</option>";
        } else {output = output+"<option value='reach'>Reach</option>";}  

        if(counselorChancing=='Far Reach') {
          output = output+"<option value='far_reach' selected='true'>Far Reach</option>";
        } else {output = output+"<option value='far_reach'>Far Reach</option>";}  

        output = output+"</select>";
        output = output+"</div>";


        //-----------------------------------------------------------//
        
        output = output+"<div class='college_chancing_cell'><select class='counselor_rec standard_select' id='"+input.colleges[i][0];
        output = output+"' name='"+input.colleges[i][0]+"'>";
        
        output = output+"<option value='none'>None</option>";

        if(counselorRec=='Early Decision') {
          output = output+"<option value='early_decision' selected='true'>Early Decision</option>";
        } else {output = output+"<option value='early_decision'>Early Decision</option>";}  
        
        if(counselorRec=='Early Action') {
          output = output+"<option value='early_action' selected='true'>Early Action</option>";
        } else {output = output+"<option value='early_action'>Early Action</option>";}  
        
        if(counselorRec=='Alternate Major') {
          output = output+"<option value='alternate_major' selected='true'>Alternate Major</option>";
        } else {output = output+"<option value='alternate_major'>Alternate Major</option>";}  

        if(counselorRec=='Not Recommended') {
          output = output+"<option value='not_recommended' selected='true'>Not Recommended</option>";
        } else {output = output+"<option value='not_recommended'>Not Recommended</option>";}  
        
        output = output+"</select>";
        output = output+"</div>";


        //-----------------------------------------------------------//


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

      $('.counselor_chancing').on('change', function(e) {        
        var studentId = document.getElementById("student_id").innerHTML;
        var sendChancing = '';
        
        if ($(this).find(":selected").val() == 'very_likely') {sendChancing = 'Very Likely'}
        if ($(this).find(":selected").val() == 'likely') {sendChancing = 'Likely'}
        if ($(this).find(":selected").val() == 'target') {sendChancing = 'Target'}
        if ($(this).find(":selected").val() == 'reach') {sendChancing = 'Reach'}
        if ($(this).find(":selected").val() == 'far_reach') {sendChancing = 'Far Reach'}

        var saveData = {'student_id':studentId, 'college_name': this.id, 'chancing': sendChancing}
        saveData = JSON.stringify(saveData);

        temp = fetch('/counselor_chancing/update_chancing', {
          method: "POST",    
          body: saveData
        }).then(response=>response.text()).then(input=>{ })
      })

      $('.counselor_rec').on('change', function(e) {        
                
        var studentId = document.getElementById("student_id").innerHTML;
        var sendRec = '';
        
        if ($(this).find(":selected").val() == 'early_decision') {sendRec = 'Early Decision'}
        if ($(this).find(":selected").val() == 'early_action') {sendRec = 'Early Action'}
        if ($(this).find(":selected").val() == 'alternate_major') {sendRec = 'Alternate Major'}
        if ($(this).find(":selected").val() == 'not_recommended') {sendRec = 'Not Recommended'}        

        var saveData = {'student_id':studentId, 'college_name': this.id, 'counselor_rec': sendRec}
        saveData = JSON.stringify(saveData);

        temp = fetch('/counselor_chancing/update_rec', {
          method: "POST",    
          body: saveData
        }).then(response=>response.text()).then(input=>{ })
      })



  })

})



$("#addCollegeButton").on('click', function test() {
  
  var studentId = document.getElementById("student_id").value;
  var collegeName = document.getElementById("addCollege").value;
  var newChancing = document.getElementById('newChancing').value;
  var newMLChancing = document.getElementById('new_ml_chancing').innerHTML;

  if (newChancing=='very_likely') {newChancing = 'Very Likely'}
  if (newChancing=='likely') {newChancing = 'Likely'}
  if (newChancing=='target') {newChancing = 'Target'}
  if (newChancing=='reach') {newChancing = 'Reach'}
  if (newChancing=='far_reach') {newChancing = 'Far Reach'}

  var newRec = '';

  var newRow = '';
  newRow = newRow+"<li><div style='clear:both'>"
  newRow = newRow+"<div class='college_name_cell'>"+collegeName+"</div>";
  newRow = newRow+"<div class='college_chancing_cell'>"+"-----"+"</div>";
  newRow = newRow+"<div class='college_chancing_cell'>"+newMLChancing+"</div>";
  newRow = newRow+"<div class='college_chancing_cell'>"+"-----"+"</div>";

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


  //-----------------------------------------------------------//

  newRow = newRow+"<div class='counselor_rec_cell'><select class='counselor_rec standard_select' id='"+collegeName;
  newRow = newRow+"' name='"+collegeName+"'>";
  
  newRow = newRow+"<option value='none' hidden='true'>Select</option>";

  if(newRec=='Early Decision') {
    newRow = newRow+"<option value='early_decision' selected='true'>Early Decision</option>";
  } else {newRow = newRow+"<option value='early_decision'>Early Decision</option>";}  
  
  if(newRec=='Early Action') {
    newRow = newRow+"<option value='early_action' selected='true'>Early Action</option>";
  } else {newRow = newRow+"<option value='early_action'>Early Action</option>";}  
  
  if(newRec=='Alternate Major') {
    newRow = newRow+"<option value='alternate_major' selected='true'>Alternate Major</option>";
  } else {newRow = newRow+"<option value='alternate_major'>Alternate Major</option>";}  

  if(newRec=='Not Recommended') {
    newRow = newRow+"<option value='Not Recommended' selected='true'>Not Recommended</option>";
  } else {newRow = newRow+"<option value='not_recommended'>Not Recommended</option>";}  
  
  newRow = newRow+"</select>";
  newRow = newRow+"</div>";


  //-----------------------------------------------------------//
  

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




/*
$('.student').on('click', function(e) {
  var studentId = $(this).attr('id');

  returnedData = fetch('/counselor_chancing/load_student_data', {
    method: "POST",    
    body: JSON.stringify({ id: studentId })
  }).then(response=>response.text()).then(input=>{
  
    input = JSON.parse(input);
    document.getElementById("student_list").style.display="none";
    document.getElementById("studentInfo").style.display ="block";
    document.getElementById("colleges").style.display ="block";


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

    var output = "<table id='college_table' style='padding: 5px'><tr><td style='width:370px'><b>College</b></td><td style='width: 130px; text-align: center'><b>Student<br/>Self-Chancing</b></td><td style='width: 130px; text-align: center'><b>ML<br>Chancing</b></td><td style='width: 130px; text-align: center'><b>Committee<br>Chancing</b></td><td style='width: 130px; text-align: center'><b>Counselor<br>Chancing</b></td></tr>";
    
    for (i=0; i<input['colleges'].length; i++) {

      var setId = "";

      setId = input['colleges'][i][0].replaceAll(' ', '_');

      output = output+"<tr><td>"+input['colleges'][i][0]+"</td><td style='text-align:center'>";
      output = output+input['colleges'][i][1]+"</td><td style='text-align:center'>";
      output = output+input['colleges'][i][2]+"</td><td style='text-align:center'>";
      output = output+input['colleges'][i][3]+"</td><td style='text-align:center'>";
      output = output+"<select class='counselor_chancing' id='"+setId;
      output = output+"' name='"+setId;
      output = output+ "' style='margin-top: 3px; margin-bottom: 3px; height:24px; font-size: small;'>";
      
      output = output+"<option value='none' hidden='true'>Select</option>";
 
      if(input['colleges'][i][3]=='Very Likely') {
        output = output+"<option value='very_likely' selected='true'>Very Likely</option>";
      } else {output = output+"<option value='very_likely'>Very Likely</option>";}  
      
      if(input['colleges'][i][3]=='Likely') {
        output = output+"<option value='likely' selected='true'>Likely</option>";
      } else {output = output+"<option value='likely'>Likely</option>";}  
      
      if(input['colleges'][i][3]=='Target') {
        output = output+"<option value='target' selected='true'>Target</option>";
      } else {output = output+"<option value='target'>Target</option>";}  

      if(input['colleges'][i][3]=='Reach') {
        output = output+"<option value='reach' selected='true'>Reach</option>";
      } else {output = output+"<option value='reach'>Reach</option>";}  

      if(input['colleges'][i][3]=='Far Reach') {
        output = output+"<option value='far_reach' selected='true'>Far Reach</option>";
      } else {output = output+"<option value='far_reach'>Far Reach</option>";}  

      output = output+"</select>";
      output = output+"</td></tr>";
    }
      
    output = output+"</table>";

    document.getElementById("colleges").innerHTML = output;

  
    $('.counselor_chancing').on('change', function(e) {
    
      var studentId = document.getElementById('student_id').innerHTML;

      if ($(this).find(":selected").val() == 'very_likely') {sendChancing = 'Very Likely'}
      if ($(this).find(":selected").val() == 'likely') {sendChancing = 'Likely'}
      if ($(this).find(":selected").val() == 'target') {sendChancing = 'Target'}
      if ($(this).find(":selected").val() == 'reach') {sendChancing = 'Reach'}
      if ($(this).find(":selected").val() == 'far_reach') {sendChancing = 'Far Reach'}
    
      var saveData = {'student_id':studentId, 'college_name': this.id, 'chancing': sendChancing}

      saveData = JSON.stringify(saveData);

      temp = fetch('/counselor_chancing/update_chancing', {
        method: "POST",    
        body: saveData
      })    

    })

   })
})
*/


$('#createMapButton').on('click', function(e) {
  var studentId = document.getElementById("student_id").innerHTML;
  
  returnedData = fetch('/counselor_chancing/save_selectivity_map', {
    method: "POST",    
    body: JSON.stringify({ id: studentId })
  }).then(response=>response.text()).then(input=>{})


})