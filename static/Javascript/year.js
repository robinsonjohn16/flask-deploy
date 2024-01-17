$("form[name=year-form").submit(function (e) {
   var $form = $(this);
   var $error = $form.find(".error");
   var data = $form.serialize();
   $.ajax({
      url: "/admin/yearCheck/",
      type: "POST",
      data: data,
      dataType: "json",
      beforeSend: function () {
         $("*").css("cursor", "progress");
      },
      success: function (resp) {
         window.location.href = "/admin/subject/";
      },
      error: function (resp) {
         $error.text(resp.responseJSON.error).removeClass("error--hidden");
         // alert("Fill all the Creds");
      },
   });
   e.preventDefault();
});
