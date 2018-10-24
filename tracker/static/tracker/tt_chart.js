var margin = {top: 40, right: 40, bottom: 40, left: 40}
var width = 420
var height = 270

var y_initial = [0]
var x_initial = [""]
var Time = "None"
var Type_initial = ""

var y_in = y_initial
var x_in = x_initial
var Type = Type_initial


// Gather Categories data

var Categories = [];
for(i=0; i < document.getElementById("code_options").options.length; i++){
    Categories.push(document.getElementById("code_options").options[i].value)
};


// Gather Rework data

var Rework = ["Rework", "Not Rework"]

// Scale creation

var y_scale = d3.scaleLinear()
    .domain([0, 100])
    .range([height, 0]);

var x_scale = d3.scaleBand()
    .domain(x_in)
    .range([margin.left, width - margin.right])
    .paddingInner(0);

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
    .style("background-color", "#e3ebf7")
    .style("border", "2px solid black")

// Chart creation
svg.append("rect")
    .attr('width', (width - margin.left))
    .attr('height', height)
    .attr("transform", 'translate(' + (2*margin.left) + ',' + margin.top + ')')
    .attr("fill", "white")

var chart = svg.append('g')
    .attr('width', width)
    .attr('height', height)
    .attr("transform", 'translate(' + margin.left + ',' + margin.top + ')')

// Adding data

chart.append("g")
    .selectAll("rect")
    .data(x_in)
    .enter()
    .append("rect")
    .attr("x", function(d) {
        return x_scale(d);
    })
    .attr("y", function(d, i) {
        return y_scale(y_in[i]);
    })
    .attr("height", function(d, i){
        return y_scale(0) - y_scale(y_in[i]);
    })
    .attr("width", 25)
    .style("fill", function(d, i){
        return c_scale(y_in[i]/7);
    })

// Adding axes

chart.append("g")
    .attr("transform", "translate(0," + height + ")")
    .attr('class', 'x axis')
    .call(xAxis);

chart.append("g")
    .attr("transform", 'translate(' + margin.left + ',0)')
    .attr('class', 'y axis')
    .call(yAxis);

svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", margin.left/2)
    .attr("x", -((height + margin.top + margin.bottom)/2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .style("font-size", "20px")
    .text("Percent");


// Checkbox events

$("#Day").change(function(){
  if (this.checked){
    $("#Week").prop("checked", false);
    $("#Month").prop("checked", false);
    Time = this.value
    Get_Data(x_in, Type);
    } else{
        Time = "None"
        Get_Data(x_in, Type)
    }
})


$("#Week").change(function() {
    if (this.checked){
        $("#Day").prop("checked", false);
        $("#Month").prop("checked", false);
        Time = this.value
        Get_Data(x_in, Type);
    } else{
        Time = "None"
        Get_Data(x_in, Type)
    }
})

$("#Month").change(function() {
    if (this.checked){
        $("#Week").prop("checked", false);
        $("#Day").prop("checked", false);
        Time = this.value
        Get_Data(x_in, Type);
    } else{
        Time = "None"
        Get_Data(x_in, Type)
    }
})


$("#Category").change(function(){
    if (this.checked){
        $("#Rework").prop("checked", false);
        Type = "Categories"
        x_in = Categories;
        Get_Data(x_in, Type);
    } else if (!this.checked) {
        if ($("#Rework").prop("checked") == false){
            $("#Week").prop("checked", false);
            $("#Day").prop("checked", false);
            $("#Month").prop("checked", false);
        }
        y_in = y_initial
        x_in = x_initial
        Type = Type_initial
        var bars = chart.selectAll("rect")
            .remove()
            .exit()
            .data(x_in)

        chart.selectAll(".x")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);
    }
})

$("#Rework").change(function(){
    if (this.checked){
        $("#Category").prop("checked", false);
        Type = "Rework"
        x_in = Rework;
        Get_Data(x_in, Type);
    } else if (!this.checked) {
        if ($("#Category").prop("checked") == false){
            $("#Week").prop("checked", false);
            $("#Day").prop("checked", false);
            $("#Month").prop("checked", false);
        }
        y_in = y_initial
        x_in = x_initial
        Type = Type_initial
        var bars = chart.selectAll("rect")
            .remove()
            .exit()
            .data(x_in)

        chart.selectAll(".x")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);
    }
})

function Get_Data(x_in, Type){
    if (Type == Type_initial){
        return alert("Please select a metric for analysis!");
    }
    var url = "chart/"
    var Amount = [];
    $.ajax({
        url: url,
        data: {
            "X": Type,
            "Time": Time,
        },
        dataType: "json",
        success: function(data) {
            var x_scale = d3.scaleBand()
                .domain(x_in)
                .range([margin.left, width])
                .paddingInner(0.05);

            var xAxis = d3.axisBottom(x_scale);

            for(s in x_in){
                Amount.push(data[x_in[s]]);
            };
            var y_in = Amount;
            var bars = chart.selectAll("rect")
                .remove()
                .exit()
                .data(x_in)
            bars.enter()
                .append("rect")
                .attr("transform", 'translate(' + (2*margin.left) + ', 0)')
                .attr("x", function(d) {
                    return x_scale(d);
                })
                .attr("y", function(d, i) {
                    return height;
                })
                .attr("height", function(d, i){
                    return 0;
                })
                .attr("width", 25)
                .style("fill", function(d, i){
                    return c_scale(y_in[i]/7);
                })
                .transition()
                    .duration(500)
                    .attr("y", function(d, i) {
                        am_sum = 0;
                        for (e in Amount){
                            am_sum = am_sum + Amount[e]
                        }
                        if (am_sum == 0){
                            return height
                        }
                        return y_scale((y_in[i]/am_sum) * 100);
                    })
                    .attr("height", function(d, i){
                        am_sum = 0;
                        for (f in Amount){
                            am_sum = am_sum + Amount[f]
                        }
                        if (am_sum == 0){
                            return 0
                        }
                        return y_scale(0) - y_scale((y_in[i]/am_sum) * 100);
                    })



            svg.selectAll(".x")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);
        },
        error: function (xhr, errorThrown){
        console.log(xhr.responseText);
        console.log(errorThrown);
        }
    })
}

