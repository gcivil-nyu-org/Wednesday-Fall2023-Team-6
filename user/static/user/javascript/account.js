// button switch part
document.addEventListener("DOMContentLoaded", function () {
  var infoFields = document.querySelectorAll(".info-field");
  var editBtn = document.querySelector(".edit-btn");
  var saveBtn = document.querySelector(".save-btn");

  // Edit button click event
  editBtn.addEventListener("click", function () {
    // Enable input fields and save button
    infoFields.forEach(function (field) {
      field.disabled = false;
    });
    saveBtn.disabled = false;
    editBtn.disabled = true;
  });
});

// appointment / consultation list part
document.addEventListener("DOMContentLoaded", function () {
  var collapsibles = document.querySelectorAll(".collapsible");

  for (var i = 0; i < collapsibles.length; i++) {
    collapsibles[i].addEventListener("click", function () {
      var content = this.nextElementSibling;
      content.style.display =
        content.style.display === "block" ? "none" : "block";
      this.classList.toggle("active");

      var icon = this.querySelector(".icon");
      icon.textContent = content.style.display === "block" ? "-" : "+";
    });
  }
});

// appointment / consultation operation part
document.addEventListener("DOMContentLoaded", function () {
  var cancelButtons = document.querySelectorAll(".cancel-btn");
  var appointmentTimeSpan = document.getElementById("appointmentTimeSpan");
  var appointmentIdInput = document.getElementById("appointmentId");
  var appointmentIdType = document.getElementById("appointmentType");
  var operationType = document.getElementById("operation")

  cancelButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      var appointmentId = this.getAttribute("data-appointment-id");
      var appointmentTime = this.getAttribute("data-appointment-time");
      var appointmentType = this.getAttribute("data-appointment-type");
      var operation = this.getAttribute("data-operation")

      appointmentIdInput.value = appointmentId;
      appointmentIdType.value = appointmentType;
      operationType.value = operation
      appointmentTimeSpan.textContent = appointmentTime;
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  var rejectButtons = document.querySelectorAll(".reject-btn");

  rejectButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      if(this.getAttribute("data-target") == "#rejectModal") {
        var appointmentId = this.getAttribute("data-appointment-id");
        var appointmentTime = this.getAttribute("data-appointment-time");
        var appointmentType = this.getAttribute("data-appointment-type");
        var operation = this.getAttribute("data-operation")

        var appointmentTimeSpan = document.getElementById("appointmentTimeSpan2");
        var appointmentIdInput = document.getElementById("appointmentId2");
        var appointmentIdType = document.getElementById("appointmentType2");
        var operationType = document.getElementById("operation2")

        appointmentIdInput.value = appointmentId;
        appointmentIdType.value = appointmentType;
        operationType.value = operation
        appointmentTimeSpan.textContent = appointmentTime;
      } else if(this.getAttribute("data-target") == "#rejectRequestModal") {
          var doctor_id = this.getAttribute("data-doctor-id");
          var doctor_name = this.getAttribute("data-doctor-name");
          
          var doctor_id_input = document.getElementById("doctor_id");
          var doctor_name_span = document.getElementById("doctor_name_span");
          doctor_name_span.textContent = doctor_name;
          doctor_id_input.value = doctor_id
      }
    });
  });
});

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

// tab part
function showContent(tabName) {
  var tabs = document.querySelectorAll(".tab");
  tabs.forEach(function (tab) {
    tab.classList.remove("active-tab");
  });

  var contentElements = document.querySelectorAll(".content");
  contentElements.forEach(function (element) {
    element.style.display = "none";
  });

  var selectedTab = document.querySelector('[name="' + tabName + '"]');
  selectedTab.classList.add("active-tab");

  var selectedContent = document.getElementById(tabName + "Content");
  selectedContent.style.display = "block";
}

function loadDefaultImage(default_img){
  document.getElementById("profile_pic").src = default_img
}