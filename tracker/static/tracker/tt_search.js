$("#search_button").on("click", function(){
    var category = $("#Category_search").prop("value")
    var subcategory = $("#SubCategory_search").prop("value")
    var url = "tasks/"
    $.ajax({
        url: url,
        data: {
            "Category": category,
            "Subcategory": subcategory,
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
        }
    })
})
