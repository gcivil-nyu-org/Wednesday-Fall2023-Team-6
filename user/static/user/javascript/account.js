document.addEventListener("DOMContentLoaded", function() {
    var infoFields = document.querySelectorAll(".info-field");
    var editBtn = document.querySelector(".edit-btn");
    var saveBtn = document.querySelector(".save-btn");

    // Edit button click event
    editBtn.addEventListener("click", function() {
        // Enable input fields and save button
        infoFields.forEach(function(field) {
            field.disabled = false;
        });
        saveBtn.disabled = false;
        editBtn.disabled = true;
    });

    // Save button click event
    saveBtn.addEventListener("click", function() {
        // Disable input fields and save button
        infoFields.forEach(function(field) {
            field.disabled = true;
        });
        saveBtn.disabled = true;
        editBtn.disabled = false;
    });
});

function showContent(tabName) {
    var contentElements = document.querySelectorAll('.content');
    contentElements.forEach(function(element) {
        element.style.display = 'none';
    });

    var selectedContent = document.getElementById(tabName + 'Content');
    selectedContent.style.display = 'block';
}