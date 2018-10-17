var margin = {top: 40, right: 40, bottom: 40, left: 40}
var width = 150
var height = 150

var x_test = [0, 1, 2, 3, 4, 5]
var y_test = [2, 1, 4, 5, 3, 6]

var x_scale = d3.scaleLinear()
    .domain([0, 6])
    .range([0, width]);

var y_scale = d3.scaleLinear()
    .domain([0, 6])
    .range([height, 0]);

var c_scale = d3.scaleSequential(d3.interpolateRdBu)
    .domain([0, 1]);

var yAxis = d3.axisLeft(y_scale);
var xAxis = d3.axisBottom(x_scale);

// Chart background

var svg = d3.select("#chart")
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .attr("class", "chart")
    .style("background-color", "white")
