// home_page.js

// Use $() to ensure that this code runs after the document is ready
$(document).ready(function () {
    // Add event listener for search-form
    $("#search-form").submit(function (event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Call the function to handle the search change
        handleSearch();
    });

    $("#location-search-button").click(function (event) {
        event.preventDefault();
        handleLocationSearch();
    });

    function handleSearch() {
        // Get the search form element
        var searchForm = document.getElementById("search-form-1");

        // Check the validity of the search form
        if (searchForm.checkValidity()) {
            // Get the input value from the search form
            var inputValue = document.getElementById("general-search").value;

            // Construct the URL with the search query
            const baseURL = window.location.origin + window.location.pathname;
            var url = "?page=1";
            url += `&query=${inputValue}`;

            // Update the URL without triggering a full page reload
            window.history.pushState(null, null, baseURL + url);

            // You can add additional logic here to update the UI with search results
            // For now, let's log the search query to the console
            console.log('General Search Query:', inputValue);
        }

        return false;
    }

    function handleLocationSearch() {
        // Get the location search form element
        var locationSearchForm = document.getElementById("location-search-form");

        // Check the validity of the location search form
        if (locationSearchForm.checkValidity()) {
            // Get the input value from the location search form
            var locationValue = document.getElementById("location-search").value;

            // Construct the URL with the location search query
            const baseURL = window.location.origin + window.location.pathname;
            var url = "?page=1";
            url += `&location=${locationValue}`;

            // Update the URL without triggering a full page reload
            window.history.pushState(null, null, baseURL + url);

            // You can add additional logic here to update the UI with location search results
            // For now, let's log the location search query to the console
            console.log('Location Search Query:', locationValue);
        }

        return false;
    }

    // Check if the logout button exists on the page
    var logoutButton = $("#logout-button");

    if (logoutButton.length) {
        // Add a click event listener to the logout button
        logoutButton.on("click", function () {
            // Display an alert when the logout button is clicked
            alert("You have successfully logged out!");
        });
    }
});
