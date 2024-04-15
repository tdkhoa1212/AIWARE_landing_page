// Show the dropdown when hovering over the button
function showDropdown() {
    document.getElementById("myDropdown").classList.add("show");
}

// Hide the dropdown when moving the pointer away from the button
function hideDropdown() {
    document.getElementById("myDropdown").classList.remove("show");
}

// Add event listeners to handle mouse enter and leave events
document.getElementById("dropdownButton").addEventListener("mouseenter", showDropdown);
document.getElementById("dropdownButton").addEventListener("mouseleave", hideDropdown);

document.getElementById("myDropdown").addEventListener("mouseenter", showDropdown);
document.getElementById("myDropdown").addEventListener("mouseleave", hideDropdown);

