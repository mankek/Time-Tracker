function Team_Create() {
    var submit = document.getElementById("optional");
    var list = document.getElementById("current_team");
    var members = list.getElementsByTagName("p");
    for (var i=0; i < members.length; ++i){
        var team_mem = document.createElement("Input")
        team_mem.type = "hidden";
        team_mem.name = "team" + (i+1).toString();
        team_mem.value = members[i].innerHTML;
        submit.appendChild(team_mem);
    }
    var length = document.getElementById("team_length");
    length.value = members.length;
}


function Team_Add() {
    var self = document.getElementById("user-name").innerHTML;
    var member_name = document.getElementById("mem_name").value;
    if(!(member_name == self)){
        var mem = document.createElement("P");
        var t = document.createTextNode(member_name);
        mem.appendChild(t);
        document.getElementById("current_team").appendChild(mem);
        mem.ondblclick = function(){
            document.getElementById("current_team").removeChild(this);
        }
        document.getElementById("mem_name").value = "";
        Team_Create();
    }
}


function Team_Reset() {
    var list = document.getElementById("current_team");
    var members = list.getElementsByTagName("p");
    for (var i=0; i < members.length; ++i) {
        document.getElementById("current_team").removeChild(members[i]);
    }
    var length = document.getElementById("team_length");
    length.value = 0;
}
