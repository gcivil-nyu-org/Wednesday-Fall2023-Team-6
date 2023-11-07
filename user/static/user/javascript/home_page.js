$(document).ready(function () {

    console.log("Script loaded successfully.");
    // Add event listener for search-form-1 (Doctor search)
    $("#search-form-1").submit(function (event) {
        event.preventDefault();
        handleDoctorChange();
    });

    // Add event listener for search-form-2 (Hospital search)
    $("#search-form-2").submit(function (event) {
        event.preventDefault();
        handleHospitalSearch();
    });

    // Add event listener for Enter key press on search-form-1 input
    $("#general-search").on("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            handleDoctorChange();
        }
    });

    // Add event listener for Enter key press on search-form-2 input
    $("#general-search1").on("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            handleHospitalSearch();
        }
    });

    $("#logout-button").on("click", function (event) {
        event.preventDefault();
        handleLogout();
    });

    function handleDoctorChange() {
        var searchForm = document.getElementById("search-form-1");

        if (searchForm.checkValidity()) {
            var inputValue = document.getElementById("general-search").value;

            const baseURL = window.location.origin + '/doctor/';
            var url = "?page=1";
            url += `&primary_speciality=All&borough=All&address=All&zip=All&name=${encodeURIComponent(inputValue)}`;

            window.location.href = baseURL + url;

            console.log('Doctor Search Query:', inputValue);
        }

        return false;
    }

    function handleHospitalSearch() {
        var locationSearchForm = document.getElementById("search-form-2");

        if (locationSearchForm.checkValidity()) {
            var locationInputValue = document.getElementById("general-search1").value;

            const baseURL = window.location.origin + '/hospital/';
            var url = "?page=1";
            url += `&facility_type=All&borough=All&location=All&postal_code=All&name=${encodeURIComponent(locationInputValue)}`;

            window.location.href = baseURL + url;

            console.log('Hospital Search Query:', locationInputValue);
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

