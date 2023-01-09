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

// name drop down

function dropdown() {
  document.getElementById("dropdowninfo").classList.toggle("show");
}

// removes user from org

function remove(email){
  fetch("/removeorg", {
            method: "POST",
            body: JSON.stringify({ email: email}),
          }).then((_res) => {
              window.location.href = "/members";
          });
        
}

// changes role

function role1(email, id){
  v = document.getElementById(id).value;
  
  
      fetch("/changerole", {
                method: "POST",
                body: JSON.stringify({ email: email, role: v}),
              }).then((_res) => {
                  window.location.href = "/members";
              });
            
  }

  //creates group

  function addgroup(user){
    var group = document.getElementById("grp")
    console.log(group.value)
        fetch("/addgroup", {
                  method: "POST",
                  body: JSON.stringify({ group: group.value, email: user}),
               }).then((_res) => {
                    window.location.href = "/members";
                });
              
    }