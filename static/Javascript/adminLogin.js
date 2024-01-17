$("form[name=admin-form").submit(function (e) {
   var $form = $(this);
   var $error = $form.find(".error");
   var data = $form.serialize();
   $.ajax({
      url: "/admin/login",
      type: "POST",
      data: data,
      dataType: "json",
      beforeSend: function () {
         $("*").css("cursor", "wait");
      },
      success: function (resp) {
         window.location.href = "/admin/year/";
      },
      error: function (resp) {
         $error.text(resp.responseJSON.error).removeClass("error--hidden");
      },
   });
   e.preventDefault();
});
