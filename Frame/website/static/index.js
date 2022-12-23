function deleteTicket(ticketId) {
    fetch("/delete-ticket", {
      method: "POST",
      body: JSON.stringify({ ticketId: ticketId }),
    }).then((_res) => {
      window.location.href = "/tickets";
    });
  }


  function editTicket(ticketId) {
    fetch("/tickets", {
      method: "POST",
      body: JSON.stringify({ ticketId: ticketId, tickettitle: tickettitle, ticketbody: ticketbody, ticketowner: ticketowner, ticketsubmitter: ticketsubmitter}),
    }).then((_res) => {
      window.location.href = "/tickets";
    });
  }
