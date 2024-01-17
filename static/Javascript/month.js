$("form[name=month-form").submit(function (e) {
   var $form = $(this);
   var $error = $form.find(".error");
   var data = $form.serialize();

   $.ajax({
      url: "/user/attendanceCheck",
      type: "POST",
      data: data,
      dataType: "json",
      beforeSend: function () {
         $("*").css("cursor", "wait");
      },
      success: function (resp) {
         window.location.href = "/user/attendance";
      },
      error: function (resp) {
         $error.text(resp.responseJSON.error).removeClass("error--hidden");
      },
   });
   e.preventDefault();
});
