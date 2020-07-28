document.addEventListener("DOMContentLoaded", () => {

    var socket = new WebSocket("ws://127.0.0.1:9000");
    const allowed = true;
    const noAllowed = false;
    socket.onopen = function () {
        console.log("Соединение установлено");
    };

    socket.onclose = function (event) {
        if (event.wasClean) {
            console.log('Соединение закрыто чисто');
        } else {
            console.log('Обрыв соединения');
        }
        console.log('Код: ' + event.code + ' причина: ' + event.reason);
        var socket = new WebSocket("ws://127.0.0.1:9000");
    };

    socket.onmessage = function (event) {
        let data = JSON.parse(event.data).data;
        console.log(data);
        document.getElementById("name").innerHTML = data.name;
        document.getElementById("access").innerHTML = data.status;
        document.getElementById("date").innerHTML = data.date;
        document.getElementById("image").src = data.image;

    };

// document.getElementById("allowed").onclick = function() {
//        socket.send(JSON.stringify(allowed));
//     };
// document.getElementById("noAllowed").onclick = function() {
//       socket.send(JSON.stringify(noAllowed));
//     };

    socket.onerror = function (error) {
        console.log("Ошибка " + error.message);
        var socket = new WebSocket("ws://127.0.0.1:9000");
    };


});