var subjectGBL, contentGBL;
$(".right-btn").click(function (e) {
   let data = $(".right-select").find(":selected").val();

   e.preventDefault();

   $.ajax({
      url: "/admin/parentCalculate/",
      type: "GET",
      data: {
         percentageSelected: data,
      },
      success: function (resp) {
         window.location.reload(".left-section");
         // alert("Successfully sent the ail");
         // window.location.href = "/";
      },
      error: function (resp) {
         $error.text(resp.responseJSON.error).removeClass("error--hidden");
      },
   });
   // $(document).ajaxStop(function () {});
});

$(".left-autoFill").click(function (e) {
   e.preventDefault();
   $.ajax({
      url: "/admin/pullTeacherForm",
      type: "GET",

      success: function (resp) {
         let { subject, content } = resp;
         document.querySelector(".subject").value = subject;
         document.querySelector(".content").value = content;
         console.log(subject, content);
      },
   });
});
$(".left-btn").click(function (e) {
   let data = document.querySelector(".name").value;
   if (!data) {
      $(".error1").text("Enter Teachers Name").removeClass("error--hidden");
      return;
   }
   $.ajax({
      url: "/admin/sendMail",
      type: "GET",
      data: {
         teacherName: data,
      },
      // dataType: "json",
      success: function (resp) {
         alert("Successfully sent the mail");
         window.location.href = "/";
      },
      error: function (resp) {
         alert(resp.responseJSON.error);
         // $error.text(resp.responseJSON.error).removeClass("error--hidden");
      },
   });
});
// $(document).ajaxStop(function () {
// window.location.reload();
// $(".updatedDef").load();
// });

// document.querySelector(".subject").value = subjectGBL;
// document.querySelector(".content").value = contentGBL;
