// let year = document.querySelector("p").textContent;
let year = "TY-IT";

if (year == "TY-IT") subList = ["EIT", "AWP", "NGT", "AI", "LA"];
if (year == "SY-IT") subList = ["AM", "PP", "DBMS", "DS", "CN"];
if (year == "FY-IT") subList = ["WP", "DM", "CS", "IP", "DM"];

subList.forEach((element) => {
   console.log(element);
   fetch("/api/attenanceList")
      .then((res) => {
         return res.json();
      })
      .then((dat) => {
         console.log(dat);
         let ctx = document.createElement("canvas");
         const data = {
            labels: ["Present", "Absent"],
            datasets: [
               {
                  label: `Attendance of ${element}`,
                  data: [dat[element][0], dat[element][1] - dat[element][0]],
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

         let section = document.createElement("section");

         // let h3 = document.createElement("h3");
         section.innerText = `Subject ${element} - ${dat[element][0]}/${dat[element][1]}`;

         // let subj = document.createElement("h4");
         // subj.innerHTML = `${element}`;
         // let h32 = document.createElement("h3");
         // h32.innerHTML = `${dat[element][1]}`;

         // let hr = document.createElement("hr");

         let container = document.querySelector(".container");

         // section.append(h3);
         // section.append(hr);
         // section.append(h32);

         let div = document.createElement("div");
         div.classList.add("chartDiv");
         div.append(ctx);
         div.append(section);
         // div.append(subj);
         container.appendChild(div);

         // document.body.appendChild(div);
         // document.querySelector("div");
      });
});
