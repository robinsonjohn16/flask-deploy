$("form[name=subject-form").submit(function (e) {
   var $form = $(this);
   var $error = $form.find(".error");
   var data = $form.serialize();
   $.ajax({
      url: "/admin/subjectCheck/",
      type: "POST",
      data: data,
      dataType: "json",
      beforeSend: function () {
         $("*").css("cursor", "wait");
      },
      success: function (resp) {
         window.location.href = "/admin/facerecognition/";
      },
      error: function (resp) {
         $error.text(resp.responseJSON.error).removeClass("error--hidden");
         // alert("Fill all the Creds");
      },
   });
   e.preventDefault();
});
