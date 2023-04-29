
$(document).ready(function() {
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
    $('.main-content').toggleClass('active');
 
    if($(this).parent().parent().parent().hasClass('active')) {
      $(this).html("<i class='fa fa-angle-double-right' style='color:rgb(220, 220, 220)'></i>");
    }
    else {
      $(this).html("<i class='fa fa-angle-double-left' style='color:rgb(220, 220, 220)'></i>");
    }
  });  
});


function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
