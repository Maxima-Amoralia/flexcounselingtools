


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


$('#createMapButton').on('click', function(e) {

  var studentId = 'hi';
  returnedData = fetch('/counselor_chancing/save_selectivity_map', {
    method: "POST",    
    body: JSON.stringify({ id: studentId })
  }).then(response=>response.text()).then(input=>{})


})