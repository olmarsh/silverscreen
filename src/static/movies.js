// Define global variables
var page = 1;
var size = 20;
var order = "runtime-desc";
var result_count = 0;
var search = '';
var search_type = 'Title';
const socket = io();

$(document).ready(function() {  // Only runs when the document is loaded
    socket.on("connected", function(text) {  // Logs that the connection was successful and requests table.
        console.log("Connected to server");

        // Set the initial query based on the inputs
        size = document.getElementById("page-size-dropdown").value;
        order = document.getElementById("order-dropdown").value;
        search = document.getElementById("search-box").value;
        search_type = document.getElementById("search-type-selector").value;
        // Update the search box to reflect the chosen type
        document.getElementById("search-box").placeholder = 'Search by '+document.getElementById("search-type-selector").value

        // Request a table update upon first load
        socket.emit("table_request", size, page, order, search, search_type);
    });

    // Update the table when an update is received
    socket.on("table_update", function(data) {
        console.log("Table update received");

        // Set the table contents to the received contents
        document.getElementById("table").innerHTML=data.table_content;

        // Format the page count indicator
        result_count = data.result_count;
        document.getElementById("page-location").innerHTML=result_count+" results found, page "+data.page+" of "+Math.ceil(result_count/size);
    });

    // Request the table again when the page size is changed
    document.getElementById("page-size-dropdown").onchange = function() {
        size = document.getElementById("page-size-dropdown").value;

        // Limit the page size to the maximum page number
        if (page > Math.ceil(result_count/size)) {page = Math.ceil(result_count/size)}

        console.log("The page size was set to "+size)
        socket.emit("table_request", size, page, order, search, search_type);
    }

    document.getElementById("search-type-selector").onchange = function() {
        search_type = document.getElementById("search-type-selector").value;

        // Update the search box to reflect the chosen type
        document.getElementById("search-box").placeholder = 'Search by '+document.getElementById("search-type-selector").value
        console.log("The search type size was set to "+search_type)
    }

    // Request the table again when something is searched
    document.getElementById("search-box").oninput = function() {
        search = document.getElementById("search-box").value;

        // Limit the page size to the maximum page number
        if (page > Math.ceil(result_count/size)) {page = Math.ceil(result_count/size)}

        console.log("The query was made "+search)
        socket.emit("table_request", size, page, order, search, search_type);
    }

    // Request the table again when the table order is changed
    document.getElementById("order-dropdown").onchange = function() {
        order = document.getElementById("order-dropdown").value;

        console.log("The page order was set to "+order);
        socket.emit("table_request", size, page, order, search, search_type);
    }
});

// Request the appropriate page upon navigation
function nav_next() {
    console.log("Increasing page");
    page += 1;
    // Limit the page size to the maximum page number
    if (page > Math.ceil(result_count/size)) {page = Math.ceil(result_count/size)}
    socket.emit("table_request", size, page, order, search, search_type);
}
function nav_prev() {
    console.log("Decreasing page");
    page -= 1;
    // Limit the page size to the minimum page number (1)
    if (page < 1) {page = 0}
    socket.emit("table_request", size, page, order, search, search_type);
}
function nav_first() {
    console.log("Go to first page");
    page = 1;
    socket.emit("table_request", size, page, order, search, search_type);
}
function nav_last() {
    console.log("Go to last page");
    page = Math.ceil(result_count/size);
    socket.emit("table_request", size, page, order, search, search_type);
}