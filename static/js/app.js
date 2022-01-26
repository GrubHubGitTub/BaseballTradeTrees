d3.csv("/static/js/Searchable_Players_2022.csv").then(function (data) {

var players = data;
var button = d3.select("#button");
var form = d3.select("#form");
button.on("click", runEnter);
form.on("submit", runEnter);

function runEnter() {
d3.select("tbody").html("")
d3.event.preventDefault();
var inputElement = d3.select("#user-input");
var inputValue = inputElement.property("value").toLowerCase().trim();
console.log(inputValue)

var filteredData =
players.filter(players => players.Name.toLowerCase().trim().includes(inputValue));
console.log(filteredData.length)

for (var i = 0; i < filteredData.length; i++) {
      console.log(filteredData[i]['Name'])
      d3.select("tbody").insert("tr").html("<td><a href=" + Flask.url_for('player', {users_player_id: (filteredData[i]['ID'])}) + ">"
      +(filteredData[i]['Name'])+"</a></td>" +"<td>"
      +(filteredData[i]['play_debut'])+"</td>") }



};

});