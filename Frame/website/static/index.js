//modal for filter button

function openFilterModal(modal_filter1, modal_wrapper1) {
  let modal_filter = document.getElementById(modal_filter1);
  let modal_wrapper = document.getElementById(modal_wrapper1);
  modal_filter.style.display = "block";
  modal_wrapper.style.display = "block";
}

function closeFilterModal(modal_filter1, modal_wrapper1) {
  let modal_filter = document.getElementById(modal_filter1);
  let modal_wrapper = document.getElementById(modal_wrapper1);

  modal_filter.style.display = "none";
  modal_wrapper.style.display = "none";
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
                    window.location.href = "/group_management";
                });   
    }

// makes ticket editable and then submits new ticket info into db

var title = document.getElementById("title");
var body = document.getElementById("body");
var owner = document.getElementById("owner");
var submitter = document.getElementById("submitter");
var type = document.getElementById("type");
var urgency = document.getElementById("urgency");
const edit_button = document.getElementById("edit-button");
const end_button = document.getElementById("end-button");
var id = document.getElementById("id");
    
    
    
    
edit_button.addEventListener("click", function() {
        
      title.contentEditable = true;
      title.style.backgroundColor = "#dddbdb";
    
      body.contentEditable = true;
      body.style.backgroundColor = "#dddbdb";
    
      owner.contentEditable = true;
      owner.style.backgroundColor = "#dddbdb";
    
      submitter.contentEditable = true;
      submitter.style.backgroundColor = "#dddbdb";
    
      type.contentEditable = true;
     type.style.backgroundColor = "#dddbdb";
    
     urgency.contentEditable = true;
     urgency.style.backgroundColor = "#dddbdb";

    document.getElementById("end-button").hidden = false;
    
    } );
    
end_button.addEventListener("click", function() {
      title.contentEditable = false;
      body.contentEditable = false;
      owner.contentEditable = false;
      submitter.contentEditable = false;
      type.contentEditable = false;
      urgency.contentEditable = false;
      document.getElementById("end-button").hidden = true;
    
    
    
function editTicket(ticketId) {
        fetch("/ticket", {
          method: "POST",
          body: JSON.stringify({ ticketId: ticketId, title: title.textContent, body: body.textContent, owner: owner.textContent, submitter: submitter.textContent, type: type.textContent, urgency: urgency.textContent}),
        }).then((_res) => {
            window.location.href = "/ticket";
        });
      }
      editTicket(id.textContent);
    } )


//deletes ticket

function deleteTicket(ticketId) {
      fetch("/delete-ticket", {
        method: "POST",
        body: JSON.stringify({ ticketId: ticketId }),
      }).then((_res) => {
        window.location.href = "/tickets";
      });
    }

  
// filter search function, work in progess

function add_search() {
let btnval = document.getElementById("searchowner");
let finalsearch = document.getElementById("finalsearch");
let filterinput = document.getElementById("filterinput");

finalsearch.value = btnval.textContent + ": " + filterinput.value;

}

function add_search1() {
let btnval = document.getElementById("searchgroup");
let finalsearch = document.getElementById("finalsearch");
let filterinput = document.getElementById("filterinput");

finalsearch.value = btnval.textContent + ": " + filterinput.value;

}

function deleteGroup(groupId) {
  fetch("/group_management", {
    method: "POST",
    body: JSON.stringify({ groupId: groupId }),
  }).then((_res) => {
    window.location.href = "/group_management";
  });
}