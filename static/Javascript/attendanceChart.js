// let year = document.querySelector("p").textContent;
let year = "TY-IT";

if (year == "TY-IT") subList = ["EIT", "AWP", "NGT", "AI", "LA"];
if (year == "SY-IT") subList = ["AM", "PP", "DBMS", "DS", "CN"];
if (year == "FY-IT") subList = ["WP", "DM", "CS", "IP", "DM"];

// console.log(Array.from(chartYear));
// console.log(typeof attedanceList);

// atted = JSON.parse(attedanceList);
// console.log(atted);
// console.log(typeof atted);
// setTimeout(3000);

subList.forEach((element) => {
   console.log(element);
   fetch("/api/attenanceList")
      .then((res) => {
         return res.json();
      })
      .then((dat) => {
         console.log(dat);
         // console.log("Array 1", dat["AI"]);
         // const ctx = document.getElementById("myChart");
         let ctx = document.createElement("canvas");
         const data = {
            labels: ["Present", "Absent"],
            datasets: [
               {
                  label: `Attendance of ${element}`,
                  data: [dat[element][0], dat[element][1] - dat[element][0]],
                  // data: [attendance_number, total_attendance - attendance_number],
                  // data: [20, 30 - 20],
                  backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
                  hoverOffset: 10,
               },
            ],
         };
         new Chart(ctx, {
            type: "pie",
            data,
            // options: {
            //    height: 1000,
            //    width: 1000,
            // },
            // responsive: true,
            // maintainAspectRatio: false,
         });

         // ctx.height = 500;
         // ctx.width = 500;

         let section = document.createElement("section");
         let h3 = document.createElement("h3");
         h3.innerText = `${dat[element][0]}`;

         let subj = document.createElement("h4");
         subj.innerHTML = `${element}`;
         let h32 = document.createElement("h3");
         h32.innerHTML = `${dat[element][1]}`;

         let hr = document.createElement("hr");
         section.append(h3);
         section.append(hr);
         section.append(h32);

         let div = document.createElement("div");
         div.append(ctx);
         div.append(section);
         div.append(subj);
         document.body.appendChild(div);
         // document.querySelector("div");
      });
});
// document.querySelectorAll("canvas").style.width = "200px";
// document.querySelectorAll("canvas").style.height = "200px";
// const ctx = document.getElementById("myChart");
// const data = {
//    labels: ["Red", "Blue"],
//    datasets: [
//       {
//          label: "My First Dataset",
//          data: [300, 50],
//          backgroundColor: [
//             "rgb(255, 99, 132)",
//             "rgb(54, 162, 235)",
//             "rgb(255, 205, 86)",
//          ],
//          hoverOffset: 4,
//       },
//    ],
// };
// new Chart(ctx, {
//    type: "pie",
//    data,
// });
