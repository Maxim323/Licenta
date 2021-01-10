console.log("socketio.js loaded.");
var socket;

function doSomething(){
    socket.emit('showMsgInConsole', myMsg="Tralala..........");
}


$(document).ready(function () {
  //connect to the socket server
    socket = io.connect('http://' + document.domain + ':' + location.port + '/');

    socket.on('showAlert', function (msg) {
        alert(msg.data);
    });
});
