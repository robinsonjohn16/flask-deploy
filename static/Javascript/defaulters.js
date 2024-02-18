function GenerateGraph(percent) {
   fetch("/api/attendancePercentMon")
      .then((res) => {
         return res.json();
      })
      .then((dat) => {
         let cleared = 0,
            notCleared = 0;
         for (const roll in dat) {
            if (dat[roll] > percent) {
               cleared++;
            } else {
               notCleared++;
            }
         }
         // console.log(`${roll} and ${dat[roll]}`);
         let ctx = document.createElement("canvas");
         const data = {
            labels: ["Present %", "Absent %"],
            datasets: [
               {
                  label: `Attendance`,
                  // data: [dat[element][0], dat[element][1] - dat[element][0]],
                  data: [cleared, notCleared],
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
         new Chart(ctx, {
            type: "doughnut",
            data,
         });
         const table_data = document.querySelector(".right-section");
         table_data.append(ctx);
         // });
         // }
      });
}
document.querySelector(".right-btn").addEventListener("click", (e) => {
   const percent = document.querySelector(".right-select").value;
   // let percent = e.val;
   if (percent !== "Select Options") GenerateGraph(percent);
});
