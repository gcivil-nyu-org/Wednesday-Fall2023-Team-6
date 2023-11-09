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
  var appointmentTimeSpan = document.getElementById("appointmentTimeSpan2");
  var appointmentIdInput = document.getElementById("appointmentId2");
  var appointmentIdType = document.getElementById("appointmentType2");
  var operationType = document.getElementById("operation2")

  rejectButtons.forEach(function (button) {
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
