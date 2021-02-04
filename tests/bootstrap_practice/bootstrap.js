const my_alert = document.querySelector(".my-alert");
const my_graph = document.querySelector(".my-graph");
const my_calendar = document.querySelector(".my-calendar");
const my_button1 = document.querySelector(".test-button1");
const my_button2 = document.querySelector(".test-button2");

console.log(my_graph);
console.log(my_calendar);


// smooth main section transition
my_graph.addEventListener('mouseenter', (e) => {
  console.log("mouse over my_graph")
  my_graph.classList.add("col-md-8");
  my_graph.classList.remove("col-md-4");
  my_calendar.classList.add("col-md-4");
  my_calendar.classList.remove("col-md-8");
})
my_calendar.addEventListener('mouseenter', (e) => {
  console.log("mouse over my_calendar")
  my_calendar.classList.add("col-md-8");
  my_calendar.classList.remove("col-md-4");
  my_graph.classList.add("col-md-4");
  my_graph.classList.remove("col-md-8");
})

// activate alert
my_button1.addEventListener('click', (e) => {
  my_alert.innerHTML = "Success"
  my_alert.classList.remove("invisible");
  my_alert.classList.remove("alert-danger");
  my_alert.classList.add("alert-success");
  setTimeout(() => {
    my_alert.classList.add("invisible");
    console.log("restore working");
  }, 2000);
})
my_button2.addEventListener('click', (e) => {
  my_alert.innerHTML = "Danger"
  my_alert.classList.remove("invisible");
  my_alert.classList.remove("alert-success");
  my_alert.classList.add("alert-danger");
  setTimeout(() => {
    my_alert.classList.add("invisible");
    console.log("restore working");
  }, 2000);
})


// chart.js
var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45]
        }]
    },

    // Configuration options go here
    options: {
      responsive: false,
      maintainAspectRatio: false,
    }
});
console.log("chart");
console.log(chart);