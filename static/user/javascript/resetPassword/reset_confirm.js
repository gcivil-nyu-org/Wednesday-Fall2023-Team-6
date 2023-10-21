function checkPassword() {

    if(document.getElementById("password").value.length < 8) {
        document.getElementById("password_status").textContent = "Password should be atleast 8 characters!";
        document.getElementById("btn_reset_password").disabled = true;
        return;
    }else {
        document.getElementById("password_status").textContent = " ";
    }
    
    if(document.getElementById("confirm-password").value != document.getElementById("password").value) {
        document.getElementById("password_status").textContent = "Password do not match!";
        document.getElementById("btn_reset_password").disabled = true;
        return;
    }else {
        document.getElementById("password_status").textContent = " ";
    }

    document.getElementById("btn_reset_password").disabled = false;
}