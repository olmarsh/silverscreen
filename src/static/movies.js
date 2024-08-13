// Open websocket
const socket = io();

socket.on("connected", function(text) {  // Logs that the connection was successful 
    console.log("connected", text);
});
