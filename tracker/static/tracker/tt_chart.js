var margin = {top: 40, right: 40, bottom: 40, left: 40}
var width = 300
var height = 270

// Gather data

var Categories = [];
for(i=0; i < document.getElementById("code_options").options.length; i++){
    Categories.push(document.getElementById("code_options").options[i].value)
};
var User = JSON.parse(document.getElementById('user-data').textContent);
var url = "chart/"
$("#test").on("click", function(){
    $.ajax({
        url: url,
        data: {
            "X": "Categories",
            "User": User
        },
        dataType: "json",
        success: function(data) {
            if (data.is_taken) {
                console.log(data.results);
            }
            else {
                alert("nothing");
            }
        },
        error: function (xhr, errorThrown){
        console.log(xhr.responseText);
        console.log(errorThrown);
        }
    })
})


var y_test = [2, 1]

var x_scale = d3.scaleBand()
    .domain(Categories)
    .range([margin.left, width - margin.right])
    .paddingInner(0.05);

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

// Chart creation

var chart = svg.append('g')
    .attr('width', width)
    .attr('height', height)
    .attr("transform", 'translate(' + (margin.left) + ',' + (margin.top) + ')')

// Adding data

chart.append("g")
    .selectAll("rect")
    .data(Categories)
    .enter()
    .append("rect")
    .attr("x", function(d) {
        return x_scale(d);
    })
    .attr("y", function(d, i) {
        return y_scale(y_test[i]);
    })
    .attr("height", function(d, i){
        return y_scale(0) - y_scale(y_test[i]);
    })
    .attr("width", 25)
    .style("fill", function(d, i){
        return c_scale(y_test[i]/7);
    })

// Adding axes

svg.append("g")
    .attr("transform", "translate(0," + (height + margin.top) + ")")
    .attr("class", "main axis date")
    .call(xAxis);

svg.append("g")
    .attr("transform", 'translate(' + margin.left + ',' + margin.top + ')')
    .attr('class', 'main axis date')
    .call(yAxis);