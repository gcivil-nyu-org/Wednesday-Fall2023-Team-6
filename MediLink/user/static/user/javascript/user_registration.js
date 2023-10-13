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