//modal for filter button

function openFilterModal() {
  let modal_filter = document.getElementById("modal-filter");
  let modal_wrapper = document.getElementById("modal-wrapper-filter");

  modal_filter.style.display = "block";
  modal_wrapper.style.display = "block";
}

function closeFilterModal() {
  let modal_filter = document.getElementById("modal-filter");
  let modal_wrapper = document.getElementById("modal-wrapper-filter");

  modal_filter.style.display = "none";
  modal_wrapper.style.display = "none";
}

let modal_filter = document.getElementById("modal-filter");
let modal_wrapper = document.getElementById("modal-wrapper-filter");

window.onclick = function(event) {
  if (event.target == modal_wrapper) {
    modal_wrapper.style.display = "none";
    modal_filter.style.display = "none";
  }
}