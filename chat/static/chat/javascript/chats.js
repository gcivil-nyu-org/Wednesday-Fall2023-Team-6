// Handle incoming messages from WebSocket
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    var div = document.createElement("p");
    if(data.sender == current_user){
        div.innerHTML = '<b>You:</b> ' + data.message;
        div.classList.add("sent");
        console.log(data.has_attachment)
        if(data.has_attachment == "yes"){
            div.innerHTML += "<br/><a href=\"#\" onclick=\"reloadPage()\">Reload page to view attachment</a>"
        }
        document.querySelector('#chat-log').appendChild(div);
    }else {
        div.innerHTML = '<b>' + sender + ":</b> " + data.message;
        div.classList.add("received");
        if(data.has_attachment == "yes"){
            div.innerHTML += `<br/><a href=\"${reload_url}\"">Reload page to view attachment</a>`
        }
        document.querySelector('#chat-log').appendChild(div);
    }
    scrollBottom(document.getElementById("chat-log"));
    if(document.getElementById("no_message")) {
        document.getElementById("no_message").style.display = 'none';
    }
};

function scrollBottom(ele) {
    ele.scrollTop = ele.scrollHeight;
    window.scrollTo(0, document.body.scrollHeight);
}

scrollBottom(document.getElementById("chat-log"));

document.querySelector('#chat-form').addEventListener('submit', function(e) {
    const messageInput = document.querySelector('#id_message');
    const fileInput = document.querySelector('#id_attachment');
    const message = messageInput.value.trim();
    const file = fileInput.files[0];

    message_object = {
        'content': message,
        'has_attachment': "no"
    }

    // If there's a file attached, let the form submit normally
    if (file) {
        message_object['has_attachment'] = "yes";
    }else {
        e.preventDefault();
        messageInput.value = '';
    }

    // If there's no file, prevent the default form submission and send via WebSocket
    if (message) {
        chatSocket.send(JSON.stringify(message_object));
    }

});

var fileInput = document.getElementById('id_attachment');
fileInput.addEventListener('change', function() {
    if(fileInput.files.length > 0){
        var fileName = fileInput.files[0].name;
        var maxFileSizeMB = 5;
        // Convert file size to megabytes
        var fileSizeMB = fileInput.files[0].size / (1024 * 1024);
        // Check if the file size is within the allowed limit
        if (fileSizeMB > maxFileSizeMB) {
            alert('Error: File size exceeds the maximum allowed size of ' + maxFileSizeMB + ' MB.');
            fileInput.value = ""
            return false; 
        }
        document.getElementById("selected_file").textContent = fileName
    }else {
        document.getElementById("selected_file").textContent = "Choose file"
    }
});