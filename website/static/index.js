function acceptRequest(username) {
    fetch("/admin/accept-request", {
      method: "POST",
      body: JSON.stringify({ username: username }),
    }).then((_res) => {
      window.location.href = "view-role-requests";
    });
  }


function rejectRequest(username) {
    fetch("/admin/reject-request", {
      method: "POST",
      body: JSON.stringify({ username: username }),
    }).then((_res) => {
      window.location.href = "view-role-requests";
    });
  }