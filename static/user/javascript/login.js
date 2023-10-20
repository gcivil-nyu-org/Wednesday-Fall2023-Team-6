function checkUserDetails() {
    if(!$("#loginForm")[0].checkValidity()){
        $("#loginForm")[0].reportValidity();
        return false;
    }

    return true;
}

// $("#loginForm").submit(function(event) {
//     event.preventDefault();
// });

// document.getElementById("btn_login_user").onclick = function(url) {
//     var url = $("#btn_login_user").attr("data-url");

//     if(document.getElementById("email").value.trim() == "" ||
//         document.getElementById("password").value.trim() == "" ||){
//         alert("Please fill the mandatory fields!");
//         return;
//     }

//     fetch(url, {
//         method: "POST",
//         credentials: 'same-origin',
//         body: JSON.stringify({
//             'date': document.getElementById("email").value,
//             'time': document.getElementById("password").value,     
//         }),
//     })
//     .then((response) => {
//         if(response.status == 200) {
//             return response.text();
//         }else {
//             throw new Error("Server Error: " + response.text());
//         }
//     })
//     .then((result) => {
//         document.getElementById("alert_message").textContent = result;
//         console.log(result);
//         $("#alert-container").show();

//         setTimeout(function() {
//             $("#alert-container").hide();
//         }, 5000);

//     })
//     .catch(error => {
//         // Handle any errors that occur during the fetch
//         alert("Error:" + error);
//     });

//     $("#loginForm").modal('hide');
// }