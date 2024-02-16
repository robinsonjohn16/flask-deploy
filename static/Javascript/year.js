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
         window.location.href = "/admin/subject";
      },
      error: function (resp) {
         $error.text(resp.responseJSON.error).removeClass("error--hidden");
         // alert("Fill all the Creds");
      },
   });
   e.preventDefault();
});

const data = {
   labels: ["Present", "Absent"],
   datasets: [
      {
         label: `Monthly Attendance`,
         data: [90, 80],
         backgroundColor: ["rgb(248,141,41)", "rgb(89,81,231)"],
         hoverBackgroundColor: ["rgb(248,141,41)", "rgb(89,81,231)"],
         hoverOffset: 10,
         circumference: 360,
         borderWidth: 0.2,
         responsive: true,
         hoverBorderColor: "#000",
      },
   ],
};
let ctx = document.createElement("canvas");
new Chart(ctx, {
   type: "doughnut",
   data,
});

let container = document.querySelector(".month-container");
let div = document.createElement("div");
div.append(ctx);
container.appendChild(div);
