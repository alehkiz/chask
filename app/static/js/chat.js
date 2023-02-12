namespace = '/chat';
var socket = io(namespace);

socket.on('connect', function() {
    console.log("conectado")
    socket.emit('my_event', {data: 'connected to the SocketServer...'});
});

socket.on('my_response', function(msg, cb) {
    console.log('Mensagem recebida: '+msg)
    $('#log').append('<br>' + $('<div/>').text('logs #' + msg.count + ': ' + msg.data).html());
    if (cb)
        cb();
});
$('form#message').submit(function(event) {
    // console.log(event)
    socket.emit('my_event', {data: $('#message-text').val()});
    console.log('Mensagem enviada: ' + $('#message-text').val())
    event.preventDefault()
    return false;
});
$('form#broadcast').submit(function(event) {
    socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
    return false;
});
$('form#disconnect').submit(function(event) {
    socket.emit('disconnect_request');
    return false;
});
