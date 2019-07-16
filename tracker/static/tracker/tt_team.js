available = document.getElementById("available");
taken = document.getElementById("current_team");
team_length = document.getElementById("team_length")
team_holder = document.getElementById("col_7")


function Team_Create() {
    var members = taken.getElementsByTagName("p");
    for (var i=0; i < members.length; ++i){
        var team_mem = document.createElement("Input")
        team_mem.type = "hidden";
        team_mem.name = "team" + (i+1).toString();
        team_mem.value = members[i].innerHTML;
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
    var last_mem = document.getElementById("col_7").lastChild
    team_holder.removeChild(last_mem)
}

function Team_Reset() {
    var list = document.getElementById("current_team");
    var members = list.getElementsByTagName("p");
    for (var i=0; i < members.length; ++i) {
        list.removeChild(members[i]);
    }
    var length = document.getElementById("team_length");
    length.value = 0;
    var team_names = document.getElementById("col_7").getElementsByTagName("input")
    for (var s=0; s < team_names.length; ++s){
        document.getElementById("col_7").removeChild(team_names[s])
    }
}
