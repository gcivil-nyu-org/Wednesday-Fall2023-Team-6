$("#booking_form").submit(function(event) {
    // this takes care of disabling the form's submission
    event.preventDefault();
});

document.getElementById("btn_confirm_details").onclick = function(url) {
    var url = $("#btn_confirm_details").attr("data-url");
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    if(document.getElementById("date").value.trim() == "" ||
        document.getElementById("time").value.trim() == "" ||
        document.getElementById("fname").value.trim() == "" ||
        document.getElementById("phone").value.trim() == "" ||
        document.getElementById("email").value.trim() == ""){
        alert("Please fill the mandatory fields!");
        return;
    }

    date_str = `${document.getElementById("date").value}T${document.getElementById("time").value}`
    given_date = new Date(date_str)
    if(given_date < Date.now()){
        alert("Please enter a valid date and time!")
        return
    }

    fetch(url, {
        method: "POST",
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            'date': document.getElementById("date").value,
            'time': document.getElementById("time").value,
            'name': document.getElementById("fname").value,
            'phone': document.getElementById("phone").value,
            'email': document.getElementById("email").value,
            'reason': document.getElementById("reason").value,
        }),
    })
    .then(response => Promise.all([response.status, response.text()]))
    .then(([status, text_message]) => {
        
        if(status == 200){
            removeClass = "alert-danger";
            addClass = "alert-success";
        }else{
            removeClass = "alert-success";
            addClass = "alert-danger"
            if(status != 400) text_message = "Error: Could not create request. Please check your details and try again!"
        }

        if(document.getElementById("alert-container").classList.contains(removeClass)){
            console.log(document.getElementById("alert-container").classList);
            document.getElementById("alert-container").classList.remove(removeClass)
        }

        if(!document.getElementById("alert-container").classList.contains(addClass))    
            document.getElementById("alert-container").classList.add(addClass)

        document.getElementById("alert_message").textContent = text_message;
        $("#alert-container").show();

    })
    .catch(error => {

        removeClass = "alert-success";
        addClass = "alert-danger"
        
        if(document.getElementById("alert-container").classList.contains(removeClass)){
            console.log(document.getElementById("alert-container").classList);
            document.getElementById("alert-container").classList.remove(removeClass)
        }

        if(!document.getElementById("alert-container").classList.contains(addClass))    
            document.getElementById("alert-container").classList.add(addClass)

        // Handle any errors that occur during the fetch
        document.getElementById("alert_message").textContent = "Error: Could not create request. Please check your details and try again!";
        $("#alert-container").show();
    });

    $("#book_appointment_modal").modal('hide');
}