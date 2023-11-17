$("#booking_form").submit(function(event) {
    event.preventDefault();
});

document.getElementById("btn_confirm_details").onclick = function(url) {
    var url = $("#btn_confirm_details").attr("data-url");
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    if(document.getElementById("date").value.trim() == "" ||
        document.getElementById("time").value.trim() == "" ||
        document.getElementById("name").value.trim() == "" ||
        document.getElementById("phone").value.trim() == "" ||
        document.getElementById("email").value.trim() == ""){
        alert("Please fill the mandatory fields!");
        return;
    }

    doctor_id = null
    if (document.getElementById("specialist").options.length > 0 && 
        document.getElementById("specialist").value != "0"){
            console.log("here")
            doctor_id = document.getElementById("specialist").value
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
            'name': document.getElementById("name").value,
            'phone': document.getElementById("phone").value,
            'email': document.getElementById("email").value,
            'reason': document.getElementById("reason").value,
            'preferred_doctor': doctor_id,
            'accebility': document.getElementById("accessibility").value,
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

function formatPhoneNumber(input) {
    var numbers = input.value.replace(/\D/g, ''); // Remove all non-digit characters
    var char = {0:'(',3:') ',6:'-'};
    input.value = '';
  
    for (var i = 0; i < numbers.length; i++) {
        input.value += (char[i] || '') + numbers[i];
    }
  
    // Validate and enable/disable the save button
    validatePhone(input);
  }
  
  function validatePhone(input) {
    var value = input.value.replace(/\D/g, ''); // Remove all non-digit characters
    var valid = value.length === 10; // Check if the length is 10 digits
  
    document.getElementById('phoneError').textContent = valid ? '' : 'Phone number must be 10 digits.';
    document.getElementById('btn_confirm_details').disabled = !valid;
  
    // Update input field style
    if (valid) {
      input.style.borderColor = "green"; // or any style for valid input
    } else {
      input.style.borderColor = "red"; // or any style for invalid input
    }
  }