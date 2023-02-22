//Add a new event to the event tables
//Event format: [index, event left, event right]
function addEvent(battle_event) {
    console.log("Debug: "+battle_event);
    //Get event table
    var table = document.getElementById('battle');
    //Add new row
    var row = table.insertRow(-1);
    row.setAttribute('class', 'row');
    //Add a cell in the new row
    var cell0 = row.insertCell(0);
    var cell1 = row.insertCell(1);
    var cell2 = row.insertCell(2);
    var cell3 = row.insertCell(3);
    cell0.setAttribute('class', 'col-1 text-end');
    cell1.setAttribute('class', 'col-5');
    cell2.setAttribute('class', 'col-1 text-end');
    cell3.setAttribute('class', 'col-5');
    //Set content of new cells
    cell0.appendChild(document.createElement('div').appendChild(document.createTextNode(battle_event[0])));
    cell1.appendChild(document.createElement('div').appendChild(document.createTextNode(battle_event[1])));
    cell2.appendChild(document.createElement('div').appendChild(document.createTextNode(battle_event[0])));
    cell3.appendChild(document.createElement('div').appendChild(document.createTextNode(battle_event[2])));

}