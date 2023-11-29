$(document).ready(function () {
    console.log("Script loaded successfully.");
    // Add event listener for the merged search form
    $("#search-form").submit(function (event) {
        event.preventDefault();
        handleSearch();
    });
    // Add event listener for Enter key press on the merged search input
    $("#general-search").on("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            handleSearch();
        }
    });
    $("#logout-button").on("click", function (event) {
        event.preventDefault();
        handleLogout();
    });
    function handleSearch() {
        var searchForm = document.getElementById("search-form");
        if (searchForm.checkValidity()) {
            var inputValue = document.getElementById("general-search").value;
            var searchType = document.getElementById("search_selector").textContent;
            var baseURL = window.location.origin;
            if (searchType.toLowerCase().includes("doctor")) {
                baseURL += '/doctor/';
                var url = `?name=${encodeURIComponent(inputValue)}`;
            } else {
                baseURL += '/hospital/';
                var url = `?name=${encodeURIComponent(inputValue)}`;
            }
            window.location.href = baseURL + url;
            console.log('Search Query:', inputValue, 'Search Type:', searchType);
        }
        return false;
    }
    function handleLogout() {
        fetch($("#logout-form").attr("action"), {
            method: $("#logout-form").attr("method"),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
            },
            body: new URLSearchParams(new FormData($("#logout-form")[0])),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            console.log("Response Content:", data);
            // Assuming the response contains a message, you can customize this part
            showLogoutMessage("Logout successful. Goodbye!");
        })
        .catch(error => {
            console.error("Logout Error:", error.message);
        });
    }
    function showLogoutMessage(message) {
        // Display the flash message to the user
        alert(message); // You can use other methods to display the message as well
    }
});

function setSelection(selection) {
    if(selection == 'doctor'){
        document.getElementById("search_selector").textContent = "Doctors ";
    }else {
        document.getElementById("search_selector").textContent = "Hospitals ";
    }
}

function carousel_left(carouselId) {
    $(`#${carouselId}`).carousel('prev');
}

function carousel_right(carouselId) {
    $(`#${carouselId}`).carousel('next');
}
