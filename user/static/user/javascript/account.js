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
