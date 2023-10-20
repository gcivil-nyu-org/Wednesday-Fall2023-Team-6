$("#booking_form").submit(function(event) {
    // this takes care of disabling the form's submission
    event.preventDefault();
});

document.getElementById("btn_confirm_details").onclick = function(url) {
    var url = $("#btn_confirm_details").attr("data-url");

    if(document.getElementById("date").value.trim() == "" ||
        document.getElementById("time").value.trim() == "" ||
        document.getElementById("fname").value.trim() == "" ||
        document.getElementById("phone").value.trim() == "" ||
        document.getElementById("email").value.trim() == ""){
        alert("Please fill the mandatory fields!");
        return;
    }

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
    .then((response) => {
        if(response.status == 200) {
            return response.text();
        }else {
            throw new Error("Server Error: " + response.text());
        }
    })
    .then((result) => {
        document.getElementById("alert_message").textContent = result;
        console.log(result);
        $("#alert-container").show();

        setTimeout(function() {
            $("#alert-container").hide();
        }, 5000);

    })
    .catch(error => {
        // Handle any errors that occur during the fetch
        alert("Error:" + error);
    });

    $("#book_appointment_modal").modal('hide');
}