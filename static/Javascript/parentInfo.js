$(".right-btn").click(function (e) {
   let data = $(".right-select").find(":selected").val();

   $.ajax({
      url: "/admin/parentCalculate/",
      type: "GET",
      data: {
         percentageSelected: data,
      },
      // dataType: "json",
      success: function (resp) {
         // window.location.href = "/admin/parentInfo#updatedDef";
      },
      // error: function (resp) {
      // $error.text(resp.responseJSON.error).removeClass("error--hidden");
      // },
   });
   e.preventDefault();
});
$(document).ajaxStop(function () {
   window.location.reload();
});
