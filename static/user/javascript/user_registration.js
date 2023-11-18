function showAdditionalFields() {
    const userType = document.getElementById("userType").value;
    document.getElementById("doctorFields").classList.add("hidden");
    document.getElementById("hospitalAdminFields").classList.add("hidden");
    document.getElementById("patientFields").classList.add("hidden");

    if (userType === "doctor") {
        document.getElementById("doctorFields").classList.remove("hidden");
        document.getElementById("hospitalAdminFields").classList.remove("hidden");
    } else if (userType === "hospital-admin") {
        document.getElementById("hospitalAdminFields").classList.remove("hidden");
    } else if (userType === "patient") {
        document.getElementById("patientFields").classList.remove("hidden");
    }
}

function checkUserDetails() {
    if(!$("#registrationForm")[0].checkValidity()){
        $("#registrationForm")[0].reportValidity();
        return false;
    }

    return true;
}

function checkPassword() {

    if(document.getElementById("password").value.length < 8) {
        document.getElementById("password_status").textContent = "Password should be atleast 8 characters!";
        document.getElementById("btn_register_user").disabled = true;
        return;
    }else {
        document.getElementById("password_status").textContent = " ";
    }
    
    if(document.getElementById("confirm-password").value != document.getElementById("password").value) {
        document.getElementById("password_status").textContent = "Password do not match!";
        document.getElementById("btn_register_user").disabled = true;
        return;
    }else {
        document.getElementById("password_status").textContent = " ";
    }

    document.getElementById("btn_register_user").disabled = false;
}

function showPasswordFields() {
    if(checkUserDetails()) {
        document.getElementById("user_details_section").classList.add("hidden");
        document.getElementById("passwordFields").classList.remove("hidden");
    }
}

$(document).ready(function () {
    const baseURL = window.location.origin;
    $('#associatedHospital').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: baseURL + '/hospital/autocomplete/',
                data: { 'search': request.term },
                dataType: 'json',
                success: function (data) {
                    response($.map(data, function (item) {
                        return {
                            label: item.name.replace(/^:/, ''),
                            value: item.id
                        };
                    }));
                }
            });
        },
        select: function (event, ui) {
            $('#associatedHospital').val(ui.item.label);
            $('#selectedId').val(ui.item.value);
            return false;
        },
        minLength: 2,
        open: function (event, ui) {
            // Add a custom class to the autocomplete menu for styling
            $(".ui-autocomplete").css("width", $('#associatedHospital').outerWidth());
            $(".ui-autocomplete").addClass("custom-autocomplete-menu");
        }
    });
});

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
    document.getElementById('continueButton').disabled = !valid;
  
    // Update input field style
    if (valid) {
      input.style.borderColor = "green"; // or any style for valid input
    } else {
      input.style.borderColor = "red"; // or any style for invalid input
    }
  }