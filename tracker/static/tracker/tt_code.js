var div = document.getElementById("code_div");
for(i=0; i < document.getElementById("subcode_options").options.length; i++){
    var lst = document.createElement("P");
    var t = document.createTextNode(document.getElementById("subcode_options").options[i].value)
    lst.appendChild(t);
    div.appendChild(lst);
};

codes = div.getElementsByTagName("p")

function Code_Search(){
    cat_in = document.getElementById("cat_search").value
    subcat_in = document.getElementById("subcat_search").value
    for (i=0; i < codes.length; i++){
        cats = codes[i].innerHTML.split(" - ")
        if (cat_in != "all" && subcat_in != "all"){
            if (cat_in != cats[0] && subcat_in != cats[1]){
                codes[i].style.display = "none";
            }
        } else{
            if (cat_in == "all" && subcat_in != "all"){
                if (subcat_in != cats[1]){
                    codes[i].style.display = "none"
                }
            } else if (cat_in != "all" && subcat_in == "all"){
                if (cat_in != cats[0]){
                    codes[i].style.display = "none"
                }
            } else{
                return console.log("hi")
            }
        }
    }
}

function Code_Reset(){
    for (s=0; s < codes.length; s++){
        codes[s].style.display = "block"
    };
    document.getElementById("cat_search").value = "all";
    document.getElementById("subcat_search").value = "all";
}