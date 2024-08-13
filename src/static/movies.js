$(document).ready(function() {  // Only runs when the document is loaded
    const socket = io();

    socket.on("connected", function(text) {  // Logs that the connection was successful and requests table.
        console.log("Connected to server");

        // Request a table update upon first load
        socket.emit("table_request");
    });

    socket.on("table_update", function(contents) {
        console.log("Table update received");

        // Set the table contents to the received contents
        document.getElementById("table").innerHTML=contents;
    });

});