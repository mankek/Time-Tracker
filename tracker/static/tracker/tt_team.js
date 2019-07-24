// no jquery here, because all the needed employee information (username, first name, last name) is sent to the frontend


// element holding available team members
available = document.getElementById("available");
// element holding chosen team members
taken = document.getElementById("current_team");
// element holding the length of the team
team_length = document.getElementById("team_length")
// element holding the taken element
team_holder = document.getElementById("col_8")

// for each team member in taken
// creates a hidden input corresponding to that member in team_holder element
// updates team length
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

// for the selected employee
// check that it isn't the user employee (which shouldn't be possible, but just in case)
// if it isn't, move the employee to the taken element
// and remove it from the available element
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

// for the selected team member
// move the member to the available element
// and remove it from the taken element
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

// clears the taken element
// adds all team members back to the available element
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

// allows a user to search available employees
// by first name, last name, or both
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

// clears any searches
// so that available element shows all available employees
function Search_Clear(){
    var all_available = available.getElementsByTagName("p")
    var name = $('#member_search').prop('value', "")
    for (var p=0; p < all_available.length; p++){
        all_available[p].style.display = "block"
    }
}


