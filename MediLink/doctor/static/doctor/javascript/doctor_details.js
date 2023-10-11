$("#booking_form").submit(function(event) {
    // this takes care of disabling the form's submission
    event.preventDefault();
});

document.getElementById("btn_confirm_details").onclick = function(url) {
    var url = $("#btn_confirm_details").attr("data-url");
    fetch(url, {
        method: "POST",
        credentials: 'same-origin',
        body: JSON.stringify({
            'date': document.getElementById("date").value,
            'time': document.getElementById("time").value,
            'name': document.getElementById("fname").value,
            'phone': document.getElementById("phone").value,
            'email': document.getElementById("email").value,
            'reason': document.getElementById("reason").value,
        }),
    })
    .then(response => response.text())
    .then(result => {
        console.log(result);
        // Handle the response from the server (e.g., display a message)
        console.log(result.message); // Replace with your handling logic
        $("#book_appointment_modal").modal('hide');
        alert("Online Booking Request Successful")
    })
    .catch(error => {
        // Handle any errors that occur during the fetch
        alert("Error:", error);
    });
}