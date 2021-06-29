
var socket;

function doSomething(){
    socket.emit('showMsgInConsole', myMsg="Tralala..........");
    console.log("button clicked")
}


function simulate_changeOfStatus(){
    console.log("Simulation started");
    lot_raw = $('#exp1').val()
    lotNr = "#" + lot_raw
    status = $('#exp3').val()

    if(status.toLowerCase()=="liber"){
        $(lotNr).attr("class", "col bg-success");
        $(lotNr).html('FREE');
        socket.emit('change_sts', sts_index=parseInt(lot_raw)-1, sts_status='LIBER')
    }

    else if(status.toLowerCase()=="ocupat"){
        $(lotNr).attr("class", "col stripes2");
        $(lotNr).html('<img class="carImg" src="/Licenta/images/car.png">');
        socket.emit('change_sts', sts_index=parseInt(lot_raw)-1, sts_status='OCUPAT')
    }



}



$(document).ready(function () {
  //connect to the socket server
    socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    console.log("socketio.js loaded.");

    socket.on('showAlert', function (msg) {
        alert(msg.data);
    });

    socket.on('lots_status', function (msg) {
        omg = JSON.parse(msg.data);
        omg = omg.slice(1, -1);
        omg = omg.split(',');
        $("#myNumber").html(omg);
    });

    socket.on('update_statistics', function (msg) {
        console.log("update_statistics request received");
        $('#free_lots').html(msg.free_lots);
        $('#occupied_lots').html(msg.occupied_lots);
        $('#undefined_lots').html(msg.undefined_lots);
        $('#occupancy_lots').html(msg.occupancy_percentage);
    });


});
