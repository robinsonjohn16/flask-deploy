// $("form[name=signup_form").submit(function (e) {
//    // var $form = $(this);
//    var $error = $form.find(".error");
//    // var data = $form.serialize();
//    var form_data = new FormData($(this));

//    $.ajax({
//       url: "/user/signup",
//       type: "POST",
//       data: form_data,
//       dataType: "json",
//       cache: false,
//       contentType: false,
//       processData: false,
//       success: function (resp) {
//          window.location.href = "/dashboard/";
//       },
//       error: function (resp) {
//          $error.text(resp.responseJSON.error).removeClass("error--hidden");
//       },
//    });

//    e.preventDefault();
// });

$(document).ready(function () {
   $("#sign-up-id").submit(function (e) {
      e.preventDefault();

      var $form = $(this);
      var $error = $form.find(".error");
      var form_data = new FormData($form[0]);

      $.ajax({
         url: "/user/signup",
         type: "POST",
         data: form_data,
         dataType: "json",
         cache: false,
         contentType: false,
         processData: false,
         beforeSend: function () {
            $("*").css("cursor", "progress");
            $(".loader").css("display", "block");
         },
         success: function (resp) {
            $(".loader").css("display", "none");
            $("*").css("cursor", "auto");

            window.location.href = "/";
         },
         error: function (resp) {
            $(".loader").css("display", "none");
            $(".normal-img").css("display", "none");
            $(".error-img").css("display", "block");
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
         },
      });
   });
});
