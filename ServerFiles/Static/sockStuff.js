"use strict";
var socket;

function doSomething(){
    socket.emit('showMsgInConsole', myMsg="Tralala..........");
    console.log("button clicked")

}


$(document).ready(function () {
  //connect to the socket server
    socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    console.log("socketio.js loaded.");

    socket.on('showAlert', function (msg) {
        alert(msg.data);
    });


    socket.on('randomNumber', function (msg) {
        console.log("number received");
        $("#myNumber").html(msg.number);
    });

});
