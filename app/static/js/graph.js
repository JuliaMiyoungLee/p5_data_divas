keys = [] 
weight = [] 

// get the timestamps 
for(let i = 0; i < graph_dictionary.length; i++){
    console.log(JSON.stringify(graph_dictionary[i]))
    const key = Object.keys(graph_dictionary[i])
    keys[i] = (key)
}
// console.log(keys.toString())

// get the weights
for(let i = 0; i < graph_dictionary.length; i++){
    current = graph_dictionary[i][keys[i]]
    weight[i] = current
}
// console.log(weight.toString())

// set up graph functionality 
var c = document.getElementById('myChart');
var ctx = c.getContext("2d")

const data = {
    labels: keys,
    datasets: [
    {
      label: "timestamps",
      data: keys,
      fill: false,
      borderColor: 'blue',
      tension: 0.1
    },
    {
      label: 'weight', 
      data: weight,
      fill:false, 
      borderColor: "red", 
      tension: 0.1 
    }
  ]
  }

  new Chart(c, {
      type: "line",
      data: data,
      options: {
        responsive: true, 
        maintainAspectRatio: true, 
        title:{
          display: true, 
          text: "Weight vs Time"
        },
        scales:{
          yAxes:[{
            scaleLabel:{
              display: true, 
              labelString: "weight (lb)",
            },
          },],
          xAxes:[{
            scaleLabel:{
              display: true, 
              labelString: "date",
            },
          },],
        },
        },
  })