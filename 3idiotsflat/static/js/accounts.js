$(document).ready(function () {
  $('#accounts_form').find('input[name="all"]').click(onAllClick);
  $('#accounts_form').find('input').click(onSingleClick);

});

function onAllClick (event) {
  if ($(this).attr("checked") == true) {
    $('#accounts_form').find('input').attr("checked", "true");
  } else {
    $('#accounts_form').find('input').removeAttr("checked");
  }
}
function onSingleClick (event) {
  if ($(this).attr("checked") == false) {
    $('#accounts_form').find('input[name="all"]').removeAttr("checked");
  }
}