var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    console.log('Connected to server');
});
socket.on('message', function(message) {
    var msg = document.createElement("p");
    msg.innerHTML = `<img src = ${message.split("-")[0]} class = "user_image"><p class = "user_message">${message.split("-")[1]}<p><br><br><br>`;
    document.getElementById('messages').appendChild(msg);
    
});
function sendMessage() {
    var message = document.getElementById('messageInput').value;
    socket.emit('message', message);
}