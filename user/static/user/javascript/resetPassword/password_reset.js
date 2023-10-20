function checkUserDetails() {
    if(!$("#resetPwdForm")[0].checkValidity()){
        $("#resetPwdForm")[0].reportValidity();
        return false;
    }

    return true;
}