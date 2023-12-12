// add event listener for filter-form
// filter.js
$("#search-form").submit(function(event) {
  event.preventDefault();
  handleFilterChange();
});

$("#filter-form").submit(function(event) {
  event.preventDefault();
  handleFilterChange();
});

function handleFilterChange() {

  var filter_form = document.getElementById("filter-form");
  var search_form = document.getElementById("search-form");
  if(filter_form.checkValidity() && search_form.checkValidity()) {
    const baseURL = window.location.origin+window.location.pathname;
    url = "?page=1";
    filters = getFilterString();
    url += filters;

    window.location.href = baseURL+url;
  }

  return false;
}

function getFilterString() {
  var filters = document.getElementById("filter-fieldset").getElementsByTagName("select");
  filter_url = "";
  
  for (let i = 0; i < filters.length; ++i) {
    let element = filters[i];
    filter_url += "&";
    filter_url += element.name;
    filter_url += "=";
    filter_url += element.value;
  }

  // Add search input
  search_name = document.getElementById("search-form").elements[0].name;
  search_value = document.getElementById("search-form").elements[0].value;
  filter_url += `&${search_name}=${search_value}`;

  return filter_url;
}


function getPageUrl(page) {
  const baseURL = window.location.origin+window.location.pathname;
  url = `?page=${page}`;
  filters = getFilterString();
  url += filters;

  window.location.href = baseURL+url;
  return false;
}

$('#contact_modal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var email = button.data('email');
  var phone = button.data('phone');
  document.getElementById("modal_email").setAttribute("href", `mailto:${email}`);
  document.getElementById("modal_email").textContent = email;
  document.getElementById("modal_phone").setAttribute("href", `tel:${phone}`);
  document.getElementById("modal_phone").textContent = phone;
});

function loadDefaultImage(default_img) {
  document.getElementById("profile_pic").src = default_img;
}