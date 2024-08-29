// Set the theme when the page loads.
window.onload = function() {
    document.body.classList.add(localStorage.getItem("theme") || "");
}

function toggle() {
    // Toggle the page theme
    document.body.classList.toggle('dark-mode');
    
    // Get the theme from local storage and update it
    theme = localStorage.getItem("theme");
    if (theme && theme === "dark-mode") {
        localStorage.setItem("theme", "");
    } else {
        localStorage.setItem("theme", "dark-mode");
    }
}

