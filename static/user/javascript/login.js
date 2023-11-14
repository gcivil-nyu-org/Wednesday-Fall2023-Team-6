function checkUserDetails() {
    if(!$("#loginForm")[0].checkValidity()){
        $("#loginForm")[0].reportValidity();
        return false;
    }

    return true;
}
