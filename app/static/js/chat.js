$(document).ready(function () {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    // var socket = io();
    socket.on('connect', function() {
        socket.emit('joined', {});
    });
    socket.on('status', function(data) {
        console.log(data)
          $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
          html = '<li class="d-flex justify-content-between mb-4 w-100">'+
            '<div class="card w-100">'+
              '<div class="card-header d-flex justify-content-between p-3">'+
                '<p class="fw-bold mb-0">' + data.name + ' Entrou na sala</p>'+
                '<p class="text-muted small mb-0"><i class="far fa-clock"></i> </p>'+
              '</div>'+
           '</div>'+
          '</li>';

          $('.messages-container').append(html)
          $('.messages-container').scrollTop($('.messages-container')[0].scrollHeight);
      });

    socket.on('my_response', function (msg, cb) {
        $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
        console.log(msg)
        if (cb)
            cb();
    });

    socket.on('message', function(data) {
        console.log(data)
          $('#chat').val($('#chat').val() + data.msg + '\n');
          html = '<li class="d-flex justify-content-between mb-4 w-100">'+
            '<img src=' + data.avatar + ' alt="avatar"'+
              'class="rounded-circle d-flex align-self-start me-3 shadow-1-strong" width="60">'+
            '<div class="card w-100">'+
              '<div class="card-header d-flex justify-content-between p-3">'+
                '<p class="fw-bold mb-0">' + data.name + '</p>'+
                '<p class="text-muted small mb-0"><i class="far fa-clock"></i> </p>'+
              '</div>'+
              '<div class="card-body">'+
                '<p class="mb-0">'+
                  data.message +
                '</p>'+
              '</div>'+
           '</div>'+
          '</li>';

          $('.messages-container').append(html)
          $('.messages-container').scrollTop($('.messages-container')[0].scrollHeight);
      });



    $('form#send-message').submit(function(event) {
        socket.emit('message_team', {data: $('#message-text').val()});
        $('#message-text').val('');
        return false;
    });

});