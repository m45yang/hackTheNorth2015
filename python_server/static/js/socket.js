// $(document).ready(function() {
//   function showMessage(message) {
//     $('#messages').html(message);
//     $('#messages').fadeIn();
//     setTimeout(function(){ $('#messages').fadeIn(); }, 3000);
//   }
//   if (!window.WebSocket) {
//       if (window.MozWebSocket) {
//           window.WebSocket = window.MozWebSocket;
//       } else {
//         showMessage("Your browser doesn't support WebSockets")
//       }
//   }
//   var ws = new WebSocket('ws://127.0.0.1:5000/echo');
//   ws.onopen = function(evt) {
//     alert('WebSocket hooked up!')
//   }
//   ws.onmessage = function(evt) {
//     showMessage(evt.data)
//   }
//   ws.onclose = function(evt) {
//       $('#messages').append('<li>WebSocket connection closed.</li>');
//   }
// });