available = document.getElementById("available");
taken = document.getElementById("current_team");
team_length = document.getElementById("team_length")
team_holder = document.getElementById("col_8")


function Team_Create() {
    var members = taken.getElementsByTagName("p");
    for (var i=0; i < members.length; ++i){
        var team_mem = document.createElement("Input")
        team_mem.type = "hidden";
        team_mem.name = "team" + (i+1).toString();
        team_mem.value = members[i].id;
        team_holder.appendChild(team_mem);
    }
    team_length.value = members.length;
}


function Team_Add(element) {
    var self = document.getElementById("user-name").innerHTML.replace(/"/g, '');
    var member_name = element.innerHTML
    if(member_name != self){
        var mem = document.createElement("P");
        mem.setAttribute("class", "employee")
        mem.setAttribute("id", element.id)
        var t = document.createTextNode(member_name);
        mem.appendChild(t);
        mem.ondblclick = function() {Team_Return(mem)};
        taken.appendChild(mem);
        available.removeChild(element)
        Team_Create();
    } else{
        var node = document.createElement("P");
        node.innerHTML = "There is no need to add yourself to a team!";
        node.setAttribute("class", "message")
        document.getElementById("message").appendChild(node);
    }
}

function Team_Return(element){
    var returned = document.createElement("P")
    returned.setAttribute("class", "employee")
    var text = document.createTextNode(element.innerHTML)
    returned.appendChild(text)
    returned.ondblclick = function() {Team_Add(returned)};
    available.appendChild(returned);
    taken.removeChild(element)
    team_length.value = team_length.value - 1;
    var last_mem = team_holder.lastChild
    team_holder.removeChild(last_mem)
}

function Team_Reset() {
    var members = taken.getElementsByTagName("p");
    for (var i=0; i < members.length; ++i) {
        Team_Return(members[i]);
    }
    var team_names = team_holder.getElementsByTagName("input")
    for (var s=0; s < team_names.length; ++s){
        team_holder.removeChild(team_names[s])
    }
    Search_Clear()
}

function Team_Search(){
    var name = $('#member_search').prop('value');
    var first_last = name.split(" ");
    var all_available = available.getElementsByTagName("p")
    for (var p=0; p < all_available.length; p++){
        emp_name = all_available[p].innerHTML.split(" ")
        if (first_last.length == 1){
            if (first_last[0] != emp_name[0] && first_last[0] != emp_name[1]){
                all_available[p].style.display = "none"
            }
        } else{
            if (first_last[0] != emp_name[0] && first_last[0] != emp_name[1] && first_last[1] != emp_name[0] && first_last[1] != emp_name[1]){
                all_available[p].style.display = "none"
            }
        }
    }
}

function Search_Clear(){
    var all_available = available.getElementsByTagName("p")
    var name = $('#member_search').prop('value', "")
    for (var p=0; p < all_available.length; p++){
        all_available[p].style.display = "block"
    }
}


