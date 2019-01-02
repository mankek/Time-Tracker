$("#search_button").on("click", function(){
    $("#tasks").empty()
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
