//  handle the pagination of active status

let page = document.getElementById("page-numbers")

let currentValue = 1


function activePage() {
    console.log(event)
    for (p of page) {
        p.classList.remove("active");
        console.log(p.classList)
    }
    event.target.classList.add("active")
    currentValue = event.target.value;
}