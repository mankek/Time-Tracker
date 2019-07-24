// jquery is used here and in tt_chart because it makes using Ajax easier
// and sending search queries to the backend is easier than having all
// the category, subcategory, and task info sent to the front-end (which is what I do for teams)

// when the search button is clicked
// search values are obtained
// and sent to the backend with an ajax request
// the response is converted to a series of <p> elements
// containing the tasks that fit the search terms
$("#search_button").on("click", function(){
    $(".task").empty()
    var category = $("#Category_search").prop("value")
    var subcategory = $("#SubCategory_search").prop("value")
    var date_s = $("#Date_search").prop("value")
    var range = []
    if ($("#on").prop("checked")) {
        range.push("on")
    }
    if ($("#before").prop("checked")) {
        range.push("before")
    }
    if ($("#after").prop("checked")) {
        range.push("after")
    }



    var url = "tasks/"
    $.ajax({
        url: url,
        data: {
            "Category": category,
            "Subcategory": subcategory,
            "Date": date_s,
            "Range": range.toString(),
        },
        dataType: "json",
        success: function(data) {
            for(i in data) {
                var task = $("<p></p>").text(data[i])
                task.attr("class", "task")
                $("#tasks").append(task)
            }
        },
        error: function(xhr, errorThrown){
            console.log(xhr.responseText)
            console.log(errorThrown)
            console.log(range)
        }
    })
})
